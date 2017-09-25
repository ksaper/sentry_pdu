from sentry.snmp_handler import SnmpHandler
from cloudshell.shell.core.context import AutoLoadResource, AutoLoadDetails, AutoLoadAttribute
from log_helper import LogHelper


class PmPduAutoloader:
    def __init__(self, context):
        self.context = context
        self.logger = LogHelper.get_logger(self.context)
        self.snmp_handler = SnmpHandler(self.context).get_raw_handler('get')

    def autoload(self):
        rv = AutoLoadDetails()
        rv.resources = []
        rv.attributes = []

        rv.attributes.append(self.makeattr('', 'Location', self.snmp_handler.get_property('SNMPv2-MIB', 'sysLocation', 0)))
        # rv.attributes.append(self.makeattr('', 'Location', self.snmp_handler.get_property('SNMPv2-MIB', 'systemLocation', 0)))
        rv.attributes.append(self.makeattr('', 'Model', self.snmp_handler.get_property('Sentry3-MIB', 'towerModelNumber', 0)))
        rv.attributes.append(self.makeattr('', 'Serial Number', self.snmp_handler.get_property('Sentry3-MIB', 'towerProductSN', 0)))
        rv.attributes.append(self.makeattr('', 'Vendor', 'Sentry'))
        rv.attributes.append(self.makeattr('', 'Version', self.snmp_handler.get_property('Sentry3-MIB', 'systemVersion', 0)))

        pdu_name = self.snmp_handler.get_property('Sentry3-MIB', 'towerName', 0)

        outlet_table = self.snmp_handler.get_table('Sentry3-MIB', 'outletTable')
        for index, attribute in outlet_table.iteritems():
            name = 'Outlet %s' % index
            relative_address = index
            unique_identifier = '%s.%s' % (pdu_name, index)

            rv.resources.append(self.makeres(name, 'Generic Power Socket', relative_address, unique_identifier))
            rv.attributes.append(self.makeattr(relative_address, 'Port Description', attribute['outletname']))

        return rv

    def makeattr(self, relative_address, attribute_name, attribute_value):
        a = AutoLoadAttribute()
        a.relative_address = relative_address
        a.attribute_name = attribute_name
        a.attribute_value = attribute_value
        return a

    def makeres(self, name, model, relative_address, unique_identifier):
        r = AutoLoadResource()
        r.name = name
        r.model = model
        r.relative_address = relative_address
        r.unique_identifier = unique_identifier
        return r
