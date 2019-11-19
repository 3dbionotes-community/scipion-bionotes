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

import pyworkflow.em

_logo = "icon.png"
_references = ['Segura2019']


class Plugin(pyworkflow.em.Plugin):

    @classmethod
    def _defineVariables(cls):
        cls._defineVar(
            'BIONOTES_WEB_ROOT_URL',
            "https://3dbionotes.cnb.csic.es/query")
        cls._defineVar(
            'BIONOTES_WS_ROOT_URL',
            "https://3dbionotes.cnb.csic.es/ws/pond/")
        cls._defineVar(
            'SENDER',
            "Scipion-EM-Bionotes")
        cls._defineVar(
            'API_KEY',
            "1731e131-b3bb-4fd4-217b-2d753e73447c")

        cls._defineVar(
            'FTP_HOST',
            "campins.cnb.csic.es")
        cls._defineVar(
            'FTP_PORT',
            "22722")
        cls._defineVar(
            'FTP_USER',
            "scipion")
        cls._defineVar(
            'FTP_PASSWORD',
            "1731e131-b3bb-4fd4-217b-2d753e73447c")


pyworkflow.em.Domain.registerPlugin(__name__)
