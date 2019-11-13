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
from pyworkflow.object import String
from pyworkflow.protocol import Protocol, params
from pyworkflow.utils.properties import Message

"""
Describe your python module here:
This module will provide the traditional Hello world example
"""

class BionotesProtocol(Protocol):
    """
    This protocol will send EM volumes and PDB models to 3DBionotes for viewing
    """
    _label = 'Viewer'

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        """ Define the input parameters that will be used.
        Params:
            form: this is the form to be populated with sections and params.
        """
        # You need a params to belong to a section:
        form.addSection(label=Message.LABEL_INPUT)
        form.addParam('inputVolume', params.PointerParam, pointerClass="Volume",
                      label='Input Volume', allowsNull=True, important=True,
                      help='Volume to be sent to 3DBionotes')

        form.addParam('atomStructure', params.PointerParam, pointerClass="AtomStruct",
                     label='Atomic structure', important=True, allowsNull=True,
                      help='Atomic structure to be sent to 3DBionotes')
        
    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        # Insert processing steps
        self._insertFunctionStep('queryBionotesStep')

    def queryBionotesStep(self):
        """"
        Query 3DBionotes WS: POST ...
        """

        # POST de atomStructure
        pdbModel = self.atomStructure.get()
        pdbModelFileName = atomStructure.getFileName()
        # 3DBionotes will return a UUID
        # UUID = request(...)
        # ...
        self.atomStructureId = String("2d753e73-217b-4fd4-b3bb-1731e131447c")

        #POST volume
        volumeMap = self.inputVolume.get()
        volumeMapFileName = volume.getFileName()
        # 3DBionotes will return a UUID
        # UUID = request(...)
        # ...
        self.volumeId = String("1fd5d9a1-986e-406d-9b4b-36b1e723fa07")
        
        # persist param values
        self._store()

    def getResultsUrl(self):

        return "https://3dbionotes.cnb.csic.es/ws/submit?volmap=%s&pdbstruct=%s" % (self.volumeId, self.atomStructureId)

    # --------------------------- INFO functions -----------------------------------
    def _summary(self):
        """ Summarize what the protocol has done"""
        summary = []

        if self.isFinished():

            summary.append("You can view results directly in 3DBionotes at %s" % self.getResultsUrl())
        return summary

    def _methods(self):
        methods = []

        if self.isFinished():
            methods.append("%s has been printed in this run %i times." % (self.message, self.times))
            if self.previousCount.hasPointer():
                methods.append("Accumulated count from previous runs were %i."
                               " In total, %s messages has been printed."
                               % (self.previousCount, self.count))
        return methods