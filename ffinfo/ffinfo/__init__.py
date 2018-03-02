#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2013 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Print compact information about a video file to standard output.

Requires ffprobe from ffmpeg.
"""

import os
import sys

container = []
streams = []


def calculate_bitrates():
    """
    Try to fill in missing bitrate information.

    If ffprobe fails to detect the bitrate of just one track, we can calculate
    that by subtracting bitrates of known tracks from the total bitrate of the
    whole file. Considering only audio and video tracks, there will be a small
    error since the space used by subtitles and the container metadata are not
    accounted for in these calculations.
    """
    total = sum(float(x["bit_rate"]) for x in container)
    astreams = [x for x in streams if x["codec_type"] == "audio"]
    vstreams = [x for x in streams if x["codec_type"] == "video"]
    known = 0
    for entry in astreams + vstreams:
        entry["bit_rate_fuzzy"] = (entry["bit_rate"] == "N/A")
        if not entry["bit_rate_fuzzy"]:
            known += float(entry["bit_rate"])
    nmissing = sum(x["bit_rate_fuzzy"]for x in astreams + vstreams)
    if nmissing > 1: return
    for entry in astreams + vstreams:
        if entry["bit_rate_fuzzy"]:
            entry["bit_rate"] = str(int(total - known))

def calculate_display_aspect_ratio(width, height, ratio):
    """Return display width, height that matches `ratio`."""
    if ratio == 0:
        return width, height
    dw = int(2 * round(max(width, ratio*height)/2))
    dh = int(2 * round(max(height, width/ratio)/2))
    return dw, dh

def comma_print(x):
    """Print `x` with a leading comma."""
    return print0("; {}".format(x))

def main(path):
    """Print information to standard output."""
    read_output(("ffprobe", "-show_format", path), container)
    read_output(("ffprobe", "-show_streams", path), streams)
    calculate_bitrates()
    print_general(path)
    print_video()
    print_audio()
    print_subtitles()

def print0(x):
    """Print `x` without a trailing newline."""
    return print(x, end="")

def print_audio():
    """Print audio track information."""
    astreams = [x for x in streams if x["codec_type"] == "audio"]
    for i, entry in enumerate(astreams):
        print0("Audio: ")
        format = entry["codec_tag_string"].lower()
        if format.find("[0]") > -1:
            format = entry["codec_name"]
        print0(format)
        if "TAG:language" in entry:
            if entry["TAG:language"] != "und":
                comma_print(entry["TAG:language"])
        bitrate = entry["bit_rate"]
        if bitrate != "N/A":
            bitrate = float(bitrate) / 1000
            bitrate = "{:.0f} kbps".format(bitrate)
            if entry["bit_rate_fuzzy"]:
                bitrate = "~" + bitrate
            comma_print(bitrate)
        channels = "{} channels".format(entry["channels"])
        channels = channels.replace("1 channels", "1 channel")
        comma_print(channels)
        print0("\n")

def print_general(path):
    """Print general information."""
    print(os.path.basename(path))
    for entry in container:
        print0(entry["format_name"])
        size = os.stat(path)[6]
        if size > 1024**3:
            size = size / 1024**3
            comma_print("{:.2f} GB".format(size))
        else:
            size = size / 1024**2
            comma_print("{:.0f} MB".format(size))
        duration = float(entry["duration"])
        comma_print(seconds_to_time(duration))
        bitrate = float(entry["bit_rate"]) / 1000
        comma_print("{:.0f} kbps".format(bitrate))
        print0("\n")

def print_subtitles():
    """Print subtitle track information."""
    sstreams = [x for x in streams if x["codec_type"] == "subtitle"]
    for i, entry in enumerate(sstreams):
        print0("Subtitles: ")
        format = entry["codec_tag_string"].lower()
        if format.find("[0]") > -1:
            format = entry["codec_name"]
        print0(format)
        if "TAG:language" in entry:
            if entry["TAG:language"] != "und":
                comma_print(entry["TAG:language"])
        print0("\n")

def print_video():
    """Print video track information."""
    vstreams = [x for x in streams if x["codec_type"] == "video"]
    for i, entry in enumerate(vstreams):
        print0("Video: ")
        format = entry["codec_tag_string"].lower()
        if format.find("[0]") > -1:
            format = entry["codec_name"]
        print0(format)
        width, height = map(int, (entry["width"], entry["height"]))
        ratio = split_field(entry["display_aspect_ratio"], ":", int)
        ratio = ratio[0] / ratio[1]
        dw, dh = calculate_display_aspect_ratio(width, height, ratio)
        resolution = "{:d}x{:d}".format(width, height)
        if dw != width or dh != height:
            resolution += " → {:d}x{:d}".format(dw, dh)
        resolution += " ({:.2f}:1)".format(dw/dh)
        comma_print(resolution)
        framerate = split_field(entry["r_frame_rate"], "/", int)
        comma_print("{:.3f} fps".format(framerate[0]/framerate[1]))
        bitrate = entry["bit_rate"]
        if bitrate != "N/A":
            bitrate = float(bitrate) / 1000
            bitrate = "{:.0f} kbps".format(bitrate)
            if entry["bit_rate_fuzzy"]:
                bitrate = "~" + bitrate
            comma_print(bitrate)
        bitrate = entry["bit_rate"]
        if bitrate != "N/A":
            bitrate = float(bitrate)
            framerate = split_field(entry["r_frame_rate"], "/", int)
            framerate = framerate[0] / framerate[1]
            bpp = bitrate / (width * height * framerate)
            bpp = "{:.3f} bpp".format(bpp)
            if entry["bit_rate_fuzzy"]:
                bpp = "~" + bpp
            comma_print(bpp)
        print0("\n")

def read_output(command, dst):
    """Read output from `command` to `dst`."""
    from subprocess import run, PIPE, DEVNULL
    output = run(command, stdout=PIPE, stderr=DEVNULL).stdout
    output = output.decode("utf_8", errors="replace")
    for line in output.splitlines():
        if line.startswith("["):
            if not line.startswith("[/"):
                dst.append({})
        elif "=" in line:
            field, value = line.split("=", 1)
            dst[-1][field] = value

def seconds_to_time(seconds):
    """Convert `seconds` to a time string."""
    return "{:02.0f}:{:02.0f}:{:02.0f}".format(
        seconds // 3600, (seconds % 3600) // 60, seconds % 60)

def split_field(value, separator, fun=lambda x: x):
    """Split `value` by `separator` and apply `fun`."""
    return list(map(fun, value.split(separator, 2)))


if __name__ == "__main__":
    if not sys.argv[1:]:
        raise SystemExit("Usage: ffinfo FILE")
    main(sys.argv[1])
