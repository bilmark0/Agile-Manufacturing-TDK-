import bpy

class GPURenderer:
    def __init__(self):
        self.set_gpu_rendering()

    def set_gpu_rendering(self):
        # Check if Cycles is enabled
        cycles_addon = bpy.context.preferences.addons.get('cycles')
        if not cycles_addon:
            print("Cycles add-on is not enabled.")
            return

        # Set rendering device to GPU
        bpy.context.scene.cycles.device = 'GPU'
        preferences = cycles_addon.preferences

        # Ensure compute device type is set
        preferences.compute_device_type = 'CUDA'  # or 'OPENCL', depending on your setup

        # Get available devices
        devices = preferences.get_devices()

        if devices is None or len(devices) == 0:
            print("No compute devices found.")
            return

        # Enable all available GPU devices
        for device in devices:
            if device.type == 'CUDA' or device.type == 'OPENCL':  # Depending on your setup
                device.use = True  # Enable the device

        print("GPU rendering has been set up.")