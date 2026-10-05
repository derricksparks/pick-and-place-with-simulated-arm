# moveit_config/

This folder is a placeholder. In M2 (MoveIt Setup Assistant), generate a full
`<pkg>_moveit_config` package with the Setup Assistant and either:

- drop its contents into this folder (simplest for a single-package project), or
- keep it as its own sibling package under `src/` if you'd rather version it separately.

Either way, update `docker/docker-compose.yml`'s mounted `src/` path is already
shared with the container, so anything added here is immediately visible inside Docker.
