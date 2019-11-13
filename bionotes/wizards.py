# -*- coding: utf-8 -*-
# **************************************************************************
# *
# * Authors:     jrmacias (jr.macias@cnb.csic.es)
# *
# * Biocomputing Unit, CNB-CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'jr.macias@cnb.csic.es'
# *
# **************************************************************************

from pyworkflow.em import ListTreeProviderString, String
import pyworkflow.gui.dialog as dialog

from bionotes.protocols import BionotesProtocol
from pyworkflow.wizard import Wizard


class BionotesWizard(Wizard):
    # Dictionary to target protocol parameters
    _targets = [(Bionotes, ['message'])]

    def show(self, form, *params):

        # This are the options:
        options = [String("Send volume map"),
                     String("Send pdb model"),
                     String("Send all")]

        # Get a data provider to be used in the tree (dialog)
        provider = ListTreeProviderString(options)

        # Show the dialog
        dlg = dialog.ListDialog(form.root, "Send models to 3DBionotes", provider,
                                "Select one of the options)")

        # Set the chosen value back to the form
        form.setVar('message', dlg.values[0].get())
