import glob
import os
import string

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
heap_model_list = ['heap_1','heap_2','heap_3','heap_4','heap_5']
heap_model = board.get(
    "build.freertos.heap_model", "heap_4")

FREE_RTOS_KERNEL_DIR = os.path.join(platform.get_package_dir(
    "framework-k1921vk-freertos"), "FreeRTOS-Kernel")

FREE_RTOS_PORT_DIR = os.path.join(
    FREE_RTOS_KERNEL_DIR, "portable", "GCC", "ARM_CM4F")

FREE_RTOS_HEAP_DIR = os.path.join(
    FREE_RTOS_KERNEL_DIR, "portable", "MemMang")


#
# add includes
#

env.Append(
    CPPPATH=[
        os.path.join(FREE_RTOS_KERNEL_DIR, "include"),
        FREE_RTOS_PORT_DIR,
        env.get("PROJECT_INCLUDE_DIR", [])
    ],
    CPPDEFINES=[
        ("FREERTOS")
    ],
)


#
# Compile FREERTOS-Kernel sources
#

sources_path = os.path.join(FREE_RTOS_KERNEL_DIR)
env.BuildSources(
    os.path.join("$BUILD_DIR", "FreeRTOS-Kernel"), sources_path,
    src_filter=[
        "+<croutine.c>",
        "+<event_groups.c>",
        "+<list.c>",
        "+<queue.c>",
        "+<stream_buffer.c>",
        "+<tasks.c>",
        "+<timers.c>"]

)

#
# Compile FREERTOS-Kernel port sources
#

sources_path = os.path.join(FREE_RTOS_PORT_DIR)
env.BuildSources(
    os.path.join("$BUILD_DIR", "FreeRTOS-Kernel-port"), sources_path,
    src_filter=[
        "+<*>"]
)

#
# Compile FREERTOS-Kernel heap_model sources
#
if heap_model in heap_model_list:
    sources_path = os.path.join(FREE_RTOS_HEAP_DIR)
    env.BuildSources(
        os.path.join("$BUILD_DIR", "FreeRTOS-Kernel-heap_model"), sources_path,
        src_filter=[
            "+<%s.c>" % heap_model]
    )
