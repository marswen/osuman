# https://github.com/OpenCodeInterpreter/OpenCodeInterpreter

import re
import threading
from jupyter_client import KernelManager
from jupyter_client.kernelspec import find_kernel_specs


class JupyterNotebook:
    def __init__(self):
        r_kernel_name = 'ir'
        kernels = find_kernel_specs()
        assert r_kernel_name in kernels
        self.km = KernelManager(kernel_name=r_kernel_name)
        self.km.start_kernel()
        self.kc = self.km.client()

    def clean_output(self, outputs):
        outputs_only_str = list()
        for i in outputs:
            if type(i) == dict:
                if "text/plain" in list(i.keys()):
                    outputs_only_str.append(i["text/plain"])
            elif type(i) == str:
                outputs_only_str.append(i)
            elif type(i) == list:
                error_msg = "\n".join(i)
                error_msg = re.sub(r"\x1b\[.*?m", "", error_msg)
                outputs_only_str.append(error_msg)

        return "\n".join(outputs_only_str).strip()

    def add_and_run(self, code_string):
        # This inner function will be executed in a separate thread
        def run_code_in_thread():
            nonlocal outputs, error_flag

            # Execute the code and get the execution count
            msg_id = self.kc.execute(code_string)

            while True:
                try:
                    msg = self.kc.get_iopub_msg(timeout=20)

                    msg_type = msg["header"]["msg_type"]
                    content = msg["content"]

                    if msg_type == "execute_result":
                        outputs.append(content["data"])
                    elif msg_type == "stream":
                        outputs.append(content["text"])
                    elif msg_type == "error":
                        error_flag = True
                        outputs.append(content["traceback"])

                    # If the execution state of the kernel is idle, it means the cell finished executing
                    if msg_type == "status" and content["execution_state"] == "idle":
                        break
                except:
                    break

        outputs = []
        error_flag = False

        # Start the thread to run the code
        thread = threading.Thread(target=run_code_in_thread)
        thread.start()

        # Wait for 20 seconds for the thread to finish
        thread.join(timeout=600)

        # If the thread is still alive after 20 seconds, it's a timeout
        if thread.is_alive():
            error_flag = True
            outputs = ["Execution timed out."]

        return self.clean_output(outputs), error_flag

    def close(self):
        """Shutdown the kernel."""
        self.km.shutdown_kernel()
