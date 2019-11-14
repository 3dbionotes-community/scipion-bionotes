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
import requests

"""
Describe your python module here:
This module will provide the traditional Hello world example
"""


WEBAPP_ROOT_URL = 'https://3dbionotes.cnb.csic.es/ws/submit'
WS_ROOT_URL = "http://campins:8700/"
API_KEY = "1731e131-b3bb-4fd4-217b-2d753e73447c"
HEADERS = {"API-Token": API_KEY}


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
        form.addParam('emVolume', params.PointerParam, pointerClass="Volume",
                      label='EM Volume', allowsNull=True, important=True,
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

        self.volumeMapId = String("")
        self.atomStructureId = String("")

        #POST volumeMap
        if self.emVolume.get():
            volumeMap = self.emVolume.get()
            volumeMapFileName = volumeMap.getLocation()
            # 3DBionotes will return a UUID
            vmFile = {'file': open(atomStructureFileName ,'rb')}
            resp = requests.post(WS_ROOT_URL + 'maps/', files=vmFile, headers=HEADERS)
            if resp.status_code == '200':
                self.volumeMapId = String(resp.text)
        # self.volumeMapId = String("31c0b23b-150a-490e-a20c-9d51374ab057")
        
        # POST atomStructure
        if self.atomStructure:
            pdbModel = self.atomStructure.get()
            atomStructureFileName = pdbModel.getFileName()
            # 3DBionotes will return a UUID
            url = WS_ROOT_URL + 'pdbs/'
            atomStructureFile = {'file': open(atomStructureFileName ,'rb')}
            resp = requests.post(url, files=atomStructureFile, headers=HEADERS)
            if resp.status_code == '200':
                self.atomStructureId = String(resp.text)
        # self.atomStructureId = String("cca40913-7079-408d-a84b-2c745d64b903")
        
        # persist param values
        self._store()

    def getResultsUrl(self):

        url = ""
        if self.volumeMapId != "":
            url += WEBAPP_ROOT_URL +"?"
            url += "volume_id=%s" % (self.volumeMapId)
            
        if self.atomStructureId != "":
            if self.volumeMapId != "":
                url += "&"
            else:
                url += WEBAPP_ROOT_URL +"?"
            url += "structure_id=%s" % (self.atomStructureId)

        return url

    # --------------------------- INFO functions -----------------------------------
    def _summary(self):
        """ Summarize what the protocol has done"""
        summary = []

        if self.isFinished():

            url = self.getResultsUrl()
            if url == "":
                summary.append("ERROR: Couldn't connect to 3DBionotes server %s" % WEBAPP_ROOT_URL)
            else:
                summary.append("You can view results directly in 3DBionotes at %s" % url)
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