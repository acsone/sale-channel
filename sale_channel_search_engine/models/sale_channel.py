# Copyright 2022 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    _sql_constraints = [
        ("se_uniq", "unique (search_engine_id)", "Only one backend per search engine")
    ]

    search_engine_id = fields.Many2one(
        comodel_name="se.backend", string="Search Engine"
    )

    def open_se_binding(self):
        action = self.env.ref("connector_search_engine.se_binding_action").read()[0]
        indexes = self.search_engine_id.index_ids.ids

        action["domain"] = [("index_id", "in", indexes)]
        return action

    def synchronize_all_indexes(self):
        for channel in self.sudo().filtered("search_engine_id"):
            indexes = channel.search_engine_id.index_ids
            bindings = indexes._add_records_from_sale_channel(channel)
            all_bindings = self.env["se.binding"].search(
                [("index_id", "in", indexes.ids)]
            )
            obsolete_bindings = all_bindings - bindings
            obsolete_bindings.write({"state": "to_delete"})
