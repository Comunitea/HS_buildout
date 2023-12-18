import base64

from odoo import http
from odoo.http import request, content_disposition
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import tempfile
import subprocess
import os

class ProjectController(http.Controller):

    @http.route('/project/report/<int:project_id>', type='http', auth='user')
    def generate_project_report(self, project_id,debug=False):
        if project_id:
            project = request.env['project.project'].browse(project_id)
            report_name = ''
            if project and project.contract_type_id:
                if project.contract_type_id.contract_type == 'mps':
                    report_name = 'hs_custom_documents.mant_puresilent_contract_report'
                elif project.contract_type_id.contract_type == 'ps':
                    report_name = 'hs_custom_documents.puresilent_contract_report'
                elif project.contract_type_id.contract_type == 'misc':
                    report_name = 'hs_custom_documents.misc_contract_report'
                elif project.contract_type_id.contract_type == 'enc':
                    report_name = 'hs_custom_documents.enc_contract_report'
                elif project.contract_type_id.contract_type == 'cap':
                    report_name = 'hs_custom_documents.cap_contract_report'
                elif project.contract_type_id.contract_type == 'rcs':
                    report_name = 'hs_custom_documents.radon_contract_report'
                else:
                    return False
                report = request.env['ir.actions.report']._get_report_from_name(report_name)
                report_output = report.render_qweb_pdf([project.id])[0]
                if project.contract_type_id.contract_conditions:
                    pdf = self.pdf_merge([base64.b64encode(report_output), project.contract_type_id.contract_conditions])
                else:
                    pdf = base64.b64encode(report_output)
                filename = report.print_report_name.replace("'","")+'-'+project.name
                response = request.make_response(base64.b64decode(pdf))
                response.headers.set('Content-Type', 'application/pdf')
                response.headers.set('Content-Disposition', content_disposition(filename))
                return response
            else:
                return False
        else:
            return False


    def pdf_merge(self, documents_pdf):
        temp_file = tempfile.NamedTemporaryFile()
        temp_file_name = temp_file.name
        merger = PdfFileMerger()
        rutas=[]
        for document_pdf in documents_pdf:
            ft = tempfile.NamedTemporaryFile()
            nft = ft.name
            fo = open(nft, "wb")
            fo.write(base64.b64decode(document_pdf))
            fo.close()
            fo = open(nft, "rb")
            merger.append(fo)
            rutas.append(fo)

        merger.write(temp_file_name)
        merger.close()
        for ruta in rutas:
            ruta.close()

        pdf = open(temp_file_name,'rb')
        result = base64.b64encode(pdf.read())
        pdf.close()
        return result

