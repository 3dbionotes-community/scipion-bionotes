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
from pyworkflow.object import Integer
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
    _label = '3DBionotes'

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        """ Define the input parameters that will be used.
        Params:
            form: this is the form to be populated with sections and params.
        """
        # You need a params to belong to a section:
        form.addSection(label=Message.LABEL_INPUT)
        form.addParam('message', params.StringParam,
                      default='Hello world!',
                      label='Message', important=True,
                      help='What will be printed in the console.')

        form.addParam('times', params.IntParam,
                      default=10,
                      label='Times', important=True,
                      help='Times the message will be printed.')

        form.addParam('previousCount', params.IntParam,
                      default=0,
                      allowsNull=True,
                      label='Previous count',
                      help='Previous count of printed messages',
                      allowsPointers=True)
    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        # Insert processing steps
        self._insertFunctionStep('greetingsStep')
        self._insertFunctionStep('createOutputStep')

    def greetingsStep(self):
        # say what the parameter says!!

        for time in range(0, self.times.get()):
            print(self.message)

    def createOutputStep(self):
        # register how many times the message has been printed
        # Now count will be an accumulated value
        timesPrinted = Integer(self.times.get() + self.previousCount.get())
        self._defineOutputs(count=timesPrinted)

    # --------------------------- INFO functions -----------------------------------
    def _summary(self):
        """ Summarize what the protocol has done"""
        summary = []

        if self.isFinished():

            summary.append("This protocol has printed *%s* %i times." % (self.message, self.times))
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