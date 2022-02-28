from xml.dom import minidom
from xml.dom.minidom import parse, Node

from numpy import record

BYTE_SIZE = {"Unsigned8": 1, "F_MessageTrailer4Byte": 4}


class XMLIsoReference:
    def __init__(self, iso_ref_object):
        self.iso_part = (
            iso_ref_object.getElementsByTagName("ISO15745Part")[0].firstChild.nodeValue,
        )
        self.iso_edition = (
            iso_ref_object.getElementsByTagName("ISO15745Edition")[
                0
            ].firstChild.nodeValue,
        )
        self.profile_technology = iso_ref_object.getElementsByTagName(
            "ProfileTechnology"
        )[0].firstChild.nodeValue


class XMLProfileHeader:
    def __init__(self, xml_header):
        iso_ref_object = xml_header.getElementsByTagName("ISO15745Reference")[0]
        iso_ref = XMLIsoReference(iso_ref_object)
        self.profile_identification = (
            xml_header.getElementsByTagName("ProfileIdentification")[
                0
            ].firstChild.nodeValue,
        )
        self.profile_revision = (
            xml_header.getElementsByTagName("ProfileRevision")[0].firstChild.nodeValue,
        )
        self.profile_name = (
            xml_header.getElementsByTagName("ProfileName")[0].firstChild.nodeValue,
        )
        self.profile_source = (
            xml_header.getElementsByTagName("ProfileSource")[0].firstChild.nodeValue,
        )
        self.profile_class = (
            xml_header.getElementsByTagName("ProfileClassID")[0].firstChild.nodeValue,
        )
        self.iso_ref = iso_ref


class XMLProfileBody:
    def __init__(self, xml_body):
        xml_device_id_object = xml_body.getElementsByTagName("DeviceIdentity")[0]

        xml_application_process_object = xml_body.getElementsByTagName(
            "ApplicationProcess"
        )[0]
        xml_device_access_point_list_object = (
            xml_application_process_object.getElementsByTagName(
                "DeviceAccessPointList"
            )[0]
        )

        self.dap_list = []

        for (
            xml_device_access_point_item_object
        ) in xml_application_process_object.getElementsByTagName(
            "DeviceAccessPointItem"
        ):
            # DEVICE MODULE INFO
            xml_device_access_point_item_module_info_object = (
                xml_device_access_point_item_object.getElementsByTagName("ModuleInfo")[
                    0
                ]
            )

            xml_module_info = XMLDeviceItemModuleInfo(
                xml_device_access_point_item_module_info_object
            )

            # MODULE LIST
            xml_device_access_point_usable_modules_object = (
                xml_device_access_point_item_object.getElementsByTagName(
                    "UseableModules"
                )[0]
            )
            xml_device_access_point_modules_object = (
                xml_application_process_object.getElementsByTagName("ModuleList")[0]
            )

            xml_device_access_point_system_defined_submodule_list_object = (
                xml_device_access_point_item_object.getElementsByTagName(
                    "SystemDefinedSubmoduleList"
                )[0]
            )

            xml_device_access_point_interface_submodule_item_object = xml_device_access_point_system_defined_submodule_list_object.getElementsByTagName(
                "InterfaceSubmoduleItem"
            )[
                0
            ]

            xml_device_access_point_port_submodule_item_object = xml_device_access_point_system_defined_submodule_list_object.getElementsByTagName(
                "PortSubmoduleItem"
            )[
                0
            ]

            self.dap_list.append(
                XMLDeviceAccessPointItem(
                    id=xml_device_access_point_item_object.getAttribute("ID"),
                    dns_compatible_name=xml_device_access_point_item_object.getAttribute(
                        "DNS_CompatibleName"
                    ),
                    module_ident_number=int(xml_device_access_point_item_object.getAttribute(
                        "ModuleIdentNumber"
                    ), 16),
                    module_info=xml_module_info,
                    usable_modules=self.calc_module_list(
                        xml_device_access_point_usable_modules_object,
                        xml_device_access_point_modules_object,
                    ),
                    interface_submodule_item=XMLInterfaceSubmoduleItem(
                        xml_device_access_point_interface_submodule_item_object
                    ),
                    port_submodule_item=XMLPortSubmoduleItem(
                        xml_device_access_point_port_submodule_item_object
                    ),
                )
            )

        self.device_identity = XMLDeviceIdentity(xml_device_id_object)

    def calc_module_list(
        self,
        xml_device_access_point_usable_modules_object,
        xml_device_access_point_modules_object,
    ):
        modules_list = []
        for (
            item_ref
        ) in xml_device_access_point_usable_modules_object.getElementsByTagName(
            "ModuleItemRef"
        ):
            for (
                module_ref
            ) in xml_device_access_point_modules_object.getElementsByTagName(
                "ModuleItem"
            ):
                if module_ref.getAttribute("ID") == item_ref.getAttribute(
                    "ModuleItemTarget"
                ):

                    modules_list.append(XMLModuleItem(module_ref, item_ref))
        return modules_list


class XMLDeviceIdentity:
    def __init__(self, xml_device_id_object):
        self.device_id = (xml_device_id_object.getAttribute("DeviceID"),)
        self.vendor_id = (xml_device_id_object.getAttribute("VendorID"),)
        self.info_text = (
            xml_device_id_object.getElementsByTagName("InfoText")[0].getAttribute(
                "TextId"
            ),
        )
        self.vendor_name = (
            xml_device_id_object.getElementsByTagName("VendorName")[0].getAttribute(
                "VendorName"
            ),
        )


class XMLDeviceItemModuleInfo:
    def __init__(self, xml_device_access_point_item_module_info_object):
        self.name = (
            xml_device_access_point_item_module_info_object.getElementsByTagName(
                "Name"
            )[0].getAttribute("TextId"),
        )
        self.info_text = (
            xml_device_access_point_item_module_info_object.getElementsByTagName(
                "InfoText"
            )[0].getAttribute("TextId"),
        )
        self.vendor_name = (
            xml_device_access_point_item_module_info_object.getElementsByTagName(
                "VendorName"
            )[0].getAttribute("Value"),
        )
        self.order_number = (
            xml_device_access_point_item_module_info_object.getElementsByTagName(
                "OrderNumber"
            )[0].getAttribute("Value"),
        )
        self.hardware_release = "1"
        self.software_release = "V4.1"


class XMLModuleItem:
    def __init__(self, module_ref, item_ref):
        xml_module_info_item = module_ref.getElementsByTagName("ModuleInfo")[0]
        xml_submodule = module_ref.getElementsByTagName("VirtualSubmoduleList")[
            0
        ].getElementsByTagName("VirtualSubmoduleItem")[0]
        xml_submodule_input = xml_submodule.getElementsByTagName("IOData")[
            0
        ].getElementsByTagName("Input")
        xml_submodule_output = xml_submodule.getElementsByTagName("IOData")[
            0
        ].getElementsByTagName("Output")
        self.id = module_ref.getAttribute("ID")
        self.module_ident_number = int(module_ref.getAttribute("ModuleIdentNumber"), 16)
        self.name = (
            xml_module_info_item.getElementsByTagName("Name")[0].getAttribute("TextId"),
        )
        self.order_number = (
            xml_module_info_item.getElementsByTagName("InfoText")[0].getAttribute(
                "TextId"
            ),
        )
        self.submododule_id = xml_submodule.getAttribute("ID")
        self.submodule_ident_number = int(
            xml_submodule.getAttribute("SubmoduleIdentNumber"), 16
        )
        self.input_length = (
            0
            if len(xml_submodule_input) == 0
            else self.add_size_io_data(
                xml_submodule_input[0].getElementsByTagName("DataItem")
            )
        )
        self.output_length = (
            0
            if len(xml_submodule_output) == 0
            else self.add_size_io_data(
                xml_submodule_output[0].getElementsByTagName("DataItem")
            )
        )
        self.input_id = (
            ""
            if len(xml_submodule_input) == 0
            else xml_submodule_input[0]
            .getElementsByTagName("DataItem")[0]
            .getAttribute("TextId")
        )
        self.output_id = (
            ""
            if len(xml_submodule_output) == 0
            else xml_submodule_output[0]
            .getElementsByTagName("DataItem")[0]
            .getAttribute("TextId")
        )
        self.datatype = (
            xml_submodule_output[0]
            .getElementsByTagName("DataItem")[0]
            .getAttribute("DataType")
            if len(xml_submodule_input) == 0
            else xml_submodule_input[0]
            .getElementsByTagName("DataItem")[0]
            .getAttribute("DataType"),
        )
        self.used_as_bits = (
            bool(
                xml_submodule_output[0]
                .getElementsByTagName("DataItem")[0]
                .getAttribute("UseAsBits")
                if len(xml_submodule_input) == 0
                else xml_submodule_input[0]
                .getElementsByTagName("DataItem")[0]
                .getAttribute("UseAsBits")
            ),
        )
        self.allowed_in_slots = item_ref.getAttribute("AllowedInSlots")
        self.used_in_slots = item_ref.getAttribute("UsedInSlots")
        self.profisafe_support = bool(xml_submodule.getAttribute("PROFIsafeSupported"))
        self.parameters = self.calc_parameter_items(xml_submodule)
        if self.profisafe_support:
            self.f_parameter = self.calc_f_parameter_items(xml_submodule)
    
    def calc_parameter_items(self, submodule):
        record_data_list = submodule.getElementsByTagName("RecordDataList")
        if len(record_data_list) > 0:
            parameter_list = record_data_list[0].getElementsByTagName(
                "ParameterRecordDataItem"
            )
            return [XMLParameterRecordDataItem(element) for element in parameter_list]
        else:
            return []

    def calc_f_parameter_items(self, submodule):
        record_data_list = submodule.getElementsByTagName("RecordDataList")
        if len(record_data_list) > 0:
            f_parameter = record_data_list[0].getElementsByTagName(
                "F_ParameterRecordDataItem"
            )[0]
            return XMLFParameterRecordDataItem(f_parameter)
        else:
            return []

    def add_size_io_data(self, data_items):
        item_size = 0
        for i in data_items:
            item_size += BYTE_SIZE[i.getAttribute("DataType")]
        return item_size

class XMLParameterRecordDataItem:
    def __init__(self, parameter_element):
        ref_item = parameter_element.getElementsByTagName("Ref")[0]
        self.index = int(parameter_element.getAttribute("Index"))
        # Length in Byte
        self.length = int(parameter_element.getAttribute("Length"))
        self.default = int(ref_item.getAttribute("DefaultValue"))
        self.min_value, self.max_value = [
            int(x) for x in ref_item.getAttribute("AllowedValues").split("..")
        ]
        self.data_type = ref_item.getAttribute("Unsigned32")
        name_item = parameter_element.getElementsByTagName("Name")[0]
        self.name = name_item.getAttribute("TextId")


class XMLFParameterRecordDataItem:
    def __init__(self, parameter_element):
        self.attributes = []
        self.index = int(parameter_element.getAttribute("Index"))
        self.paramDescCrc = int(parameter_element.getAttribute("F_ParamDescCRC"))
        for element in parameter_element.childNodes:
            if element.nodeType == minidom.Node.ELEMENT_NODE:
                attr = {}
                attr["name"] = element.nodeName
                attr["default"] = element.getAttribute("DefaultValue")
                attr["allowed_values"] = element.getAttribute("AllowedValues")
                attr["changeable"] = bool(element.getAttribute("Changeable"))
                attr["visible"] = bool(element.getAttribute("Visible"))
                self.attributes.append(attr)


class XMLInterfaceSubmoduleItem:
    def __init__(self, submodule_element):
        timing_prop_element = submodule_element.getElementsByTagName(
            "ApplicationRelations"
        )[0].getElementsByTagName("TimingProperties")[0]
        self.id = submodule_element.getAttribute("ID")
        self.subslot_number = int(submodule_element.getAttribute("SubslotNumber"))
        self.subslot_ident_number = int(
            submodule_element.getAttribute("SubmoduleIdentNumber"), 16
        )
        self.supported_rt_classes = submodule_element.getAttribute(
            "SupportedRT_Classes"
        )
        self.send_clock = timing_prop_element.getAttribute("SendClock")
        self.reduction_ratio = timing_prop_element.getAttribute("ReductionRatio")


class XMLPortSubmoduleItem:
    def __init__(self, submodule_element):
        mau_type_list = submodule_element.getElementsByTagName("MAUTypeList")[0]
        self.id = submodule_element.getAttribute("ID")
        self.subslot_number = int(submodule_element.getAttribute("SubslotNumber"))
        self.subslot_ident_number = int(
            submodule_element.getAttribute("SubmoduleIdentNumber"), 16
        )
        self.mau_type_list = [
            item.getAttribute("Value")
            for item in mau_type_list.getElementsByTagName("MAUTypeItem")
        ]


class XMLDeviceAccessPointItem:
    def __init__(
        self,
        id,
        dns_compatible_name,
        module_info,
        usable_modules,
        interface_submodule_item,
        port_submodule_item,
        conformance_class="B",
        netload_class="III",
        io_config_max_length="512",
        io_config_min_length="512",
        fixed_in_slots="0",
        physical_slots="0..2",
        min_device_interval="32",
        module_ident_number="0x00000001",
    ):
        self.id = id
        self.dns_compatible_name = dns_compatible_name
        self.module_info = module_info
        self.usable_modules = usable_modules
        self.interface_submodule_item = interface_submodule_item
        self.port_submodule_item = port_submodule_item
        self.conformance_class = conformance_class
        self.netload_class = netload_class
        self.io_config_max_length = io_config_max_length
        self.io_config_min_length = io_config_min_length
        self.fixed_in_slots = fixed_in_slots
        self.physical_slots = physical_slots
        self.min_device_interval = min_device_interval
        self.module_ident_number = module_ident_number


class XMLDevice:
    def __init__(self, path):
        self.document = parse(path)

        # PROCESS HEADER
        xml_header = self.document.getElementsByTagName("ProfileHeader")[0]
        self.header = XMLProfileHeader(xml_header)
        # END PROCESS HEADER

        # START PROCESS BODY
        xml_body = self.document.getElementsByTagName("ProfileBody")[0]
        self.body = XMLProfileBody(xml_body)
        # END PROCESS BODY


def main():
    device = XMLDevice("./gsdml/test_project.xml")


if __name__ == "__main__":
    main()
