#!/usr/bin/env python3
"""
Project 1 pick-and-place state machine.

Skeleton for M4 (see the Daily Plan doc, "M4 — Single pick-and-place").
States: APPROACH -> GRASP -> TRANSPORT -> PLACE -> RETREAT.

Fill in the MoveIt2 planning calls (moveit_py) once M1-M3 are done and
the arm/gripper/scene exist in Gazebo.
"""
import rclpy
from rclpy.node import Node


class PickPlaceNode(Node):
    def __init__(self):
        super().__init__("pick_place_node")
        self.get_logger().info("pick_place_node started (skeleton - fill in M4 logic)")
        # TODO (M4, Oct 4): load moveit_py MoveItPy instance here
        # TODO (M4, Oct 5): implement approach() / grasp()
        # TODO (M4, Oct 6): implement transport() / place() / retreat()

    def run_cycle(self, target_pose):
        """Run one pick-and-place cycle against a given object pose. Stub."""
        self.get_logger().info(f"run_cycle called with pose: {target_pose} (not yet implemented)")


def main(args=None):
    rclpy.init(args=args)
    node = PickPlaceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
