# Config

## Targets
# Do nothing.
.PHONY: null
null:
	@$(error No Default Target).

# Toolchain Includes
include .mk_inc/env.mk
include .mk_inc/host_env.mk
include .mk_inc/python.mk
include .mk_inc/arduino.mk
include .mk_inc/lint.mk
