# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SeIndex(models.Model):
    _inherit = "se.index"
    _description = "Se Index"

    def _add_records_from_sale_channel(self, channel):
        bindings = self.env["se.binding"]
        for index in self:
            index_model = index.model_id.model
            if "channel_ids" not in self.env[index_model]._fields:
                continue
            records = self.env[index_model].search([("channel_ids", "in", channel.id)])
            bindings |= records._add_to_index(index)
        return bindings
