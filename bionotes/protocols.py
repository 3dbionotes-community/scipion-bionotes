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
from bionotes import Plugin
import os
import requests
import json
import gzip


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
        form.addParam('emVolume', params.PointerParam, pointerClass="Volume",
                      label='EM Volume', allowsNull=True, important=True,
                      help='Volume to be sent to 3DBionotes')

        form.addParam('atomStructure', params.PointerParam,
                      pointerClass="AtomStruct",
                      label='Atomic structure', important=True,
                      allowsNull=True,
                      help='Atomic structure to be sent to 3DBionotes')

    # --------------------------- STEPS functions -----------------------------
    def _insertAllSteps(self):
        # Insert processing steps
        self._insertFunctionStep('queryBionotesStep')

    def queryBionotesStep(self):
        """"
        Send structure files to 3DBionotes WS
        A POST query is sent for every file. 3DBionotes will return a UUID
        that would be used to show the file in the 3D viewer.
        """
        self.volumeMapId = String("")
        self.atomStructureId = String("")

        # POST volumeMap
        if self.emVolume.get():
            volumeMap = self.emVolume.get()
            vmFileName = volumeMap.getFileName()
            vmFile = open(vmFileName, 'rb')
            if vmFileName.endswith("map"):
                # compress file
                gzFileName = vmFileName + '.gz'
                import gzip
                with open(vmFileName, 'rb') as f_in:
                    with gzip.open(gzFileName, 'wb') as f_out:
                        f_out.write(f_in.read())
                # reopen gziped file for sending
                gzFile = open(gzFileName, 'rb')
            # 3DBionotes will return a UUID
            resp = requests.post(Plugin.getVar('BIONOTES_WS_ROOT_URL')+'maps/',
                                 files={'file': gzFile},
                                 headers={
                                     "API-Token": Plugin.getVar('API_KEY'),
                                     "Sender": Plugin.getVar('SENDER'),
                                     "Title": os.path.basename(gzFileName),
                                     "Ori-Path": gzFileName})
            gzFile.close()
            if resp.status_code == 201:
                uuid = resp.json()['unique_id']
                self.volumeMapId = String(uuid)
            else:
                raise Exception(resp.status_code, resp.reason, resp.url)

        # POST atomStructure
        if self.atomStructure.get():
            pdbModel = self.atomStructure.get()
            asFileName = pdbModel.getFileName()
            assert asFileName.endswith('.cif')
            asFile = open(asFileName, 'rb')

            # compress file
            gzFileName = asFileName + '.gz'

            with open(asFileName, 'rb') as f_in:
                with gzip.open(gzFileName, 'wb') as f_out:
                    f_out.write(f_in.read())
            # reopen gziped file for sending
            gzFile = open(gzFileName, 'rb')
            # 3DBionotes will return a UUID
            resp = requests.post(Plugin.getVar('BIONOTES_WS_ROOT_URL')+'pdbs/',
                                 files={'file': gzFile},
                                 headers={
                                    "API-Token": Plugin.getVar('API_KEY'),
                                    "Sender":  Plugin.getVar('SENDER'),
                                    "Title": os.path.basename(gzFileName),
                                    "Ori-Path": gzFileName})
            gzFile.close()
            if resp.status_code == 201:
                uuid = resp.json()['unique_id']
                self.atomStructureId = String(uuid)
            else:
                raise Exception(resp.status_code, resp.reason, resp.url)

        # persist param values
        self._store()

    def getResultsUrl(self):

        url = ""
        if self.volumeMapId != "":
            url += Plugin.getVar('BIONOTES_WEB_ROOT_URL') + "?"
            url += "volume_id=%s" % (self.volumeMapId)

        if self.atomStructureId != "":
            if self.volumeMapId != "":
                url += "&"
            else:
                url += Plugin.getVar('BIONOTES_WEB_ROOT_URL') + "?"
            url += "structure_id=%s" % (self.atomStructureId)

        return url

    # --------------------------- INFO functions ------------------------------
    def _summary(self):
        """ Summarize what the protocol has done"""
        summary = []

        if self.isFinished():

            url = self.getResultsUrl()
            if url == "":
                summary.append(
                    "ERROR: Couldn't connect to 3DBionotes server %s" %
                    Plugin.getVar('BIONOTES_WEB_ROOT_URL'))
            else:
                summary.append(
                    "You can view results directly in 3DBionotes at %s" % url)
        return summary

    def _methods(self):
        methods = []

        if self.isFinished():
            methods.append(
                "%s has been printed in this run %i times." %
                (self.message, self.times))
            if self.previousCount.hasPointer():
                methods.append("Accumulated count from previous runs were %i."
                               " In total, %s messages has been printed."
                               % (self.previousCount, self.count))
        return methods
