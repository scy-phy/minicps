# from gsdml_parser import XMLDevice


class GSDMLDevice:
    def __init__(self, device):
        self.device = device

    def get_device_parameters(self, dap=0):
        used_dap = self.device.body.dap_list[0]
        used_modules = [
            element
            for element in used_dap.usable_modules
            if element.used_in_slots != ""
        ]

        parameter_to_write = [
            {
                "parameter": module.parameters,
                "f_parameter": [module.f_parameter]
                if module.profisafe_support
                else [],
            }
            for module in used_modules
        ]
        return parameter_to_write

    def get_device_parameter_count(self):
        parameters = self.get_device_parameters()
        sum_parameters = sum(
            len(item["parameter"]) + len(item["f_parameter"]) for item in parameters
        )
        return sum_parameters

    def get_interface_submodule_item(self): 
        return self.device.body.dap_list[0].interface_submodule_item

    def get_port_submodule_item(self): 
        return self.device.body.dap_list[0].port_submodule_item

    def get_port_module_ident(self): 
        return self.device.body.dap_list[0].module_ident_number

    def get_used_modules(self):
        used_dap = self.device.body.dap_list[0]
        used_modules = [
            element
            for element in used_dap.usable_modules
            if element.used_in_slots != ""
        ]
        return used_modules

    def get_output_message(self):
        pass


# def main():
#     device = Device(
#         device=XMLDevice("./gsdml/test_project_2.xml"),
#     )

#     device.get_device_parameter_count()


# if __name__ == "__main__":
#     main()
