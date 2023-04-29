# -*- coding: utf-8 -*-

from odoo import api, models, fields, _


class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    is_workspace = fields.Boolean(string='Project Workspace', help="Centralize the documents attached to this project"
                                                                   "and it tasks in one sub workspace.")
    project_settings = fields.Boolean(related="company_id.documents_project_settings")
    workspace_id = fields.Many2one('documents.folder',"Workspace",readonly=True)
    
    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        res = super(ProjectProject, self).create(vals)
        for rec in res:
            if rec.project_settings and rec.is_workspace:
                rec.workspace_id = self.env['documents.folder'].create(
                    {'name': rec.name, 'parent_folder_id': self.env.company.project_folder.id}).id
        return res

    def write(self, vals):
        res = super(ProjectProject, self).write(vals)
        for rec in self:
            if vals.get('is_workspace'):
                if not rec.workspace_id and rec.project_settings:
                    rec.workspace_id = self.env['documents.folder'].create(
                        {'name': rec.name, 'parent_folder_id': self.env.company.project_folder.id}).id
                project_documents = self.env['documents.document'].search([('res_model', '=', rec._name),
                                                                           ('res_id', '=', rec.id)])
                task_documents = self.env['documents.document'].search([('res_model', '=', 'project.task'),
                                                                        ('res_id', 'in', rec.task_ids.ids)])
                task_documents.write({'folder_id': rec.workspace_id.id})
                project_documents.write({'folder_id': rec.workspace_id.id})
            elif not vals.get('is_workspace'):
                project_documents = self.env['documents.document'].search([('res_model', '=', rec._name),
                                                                           ('res_id', '=', rec.id)])
                task_documents = self.env['documents.document'].search([('res_model', '=', 'project.task'),
                                                                        ('res_id', 'in', rec.task_ids.ids)])
                task_documents.write({'folder_id': self.env.company.project_folder.id})
                project_documents.write({'folder_id': self.env.company.project_folder.id})
        return res

    def _get_document_folder(self):
        if self.is_workspace:
            return self.workspace_id
        else:
            return super(ProjectProject,self)._get_document_folder()

    def _check_create_documents(self):
        if self.is_workspace:
            return self.workspace_id and super()._check_create_documents()
        else:
            return super(ProjectProject,self)._check_create_documents() 


class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    def write(self, vals):
        for rec in self:
            if vals.get('project_id') and rec.project_id.id != vals.get('project_id'):
                task_documents = self.env['documents.document'].search([('res_model', '=', rec._name),
                                                                        ('res_id', '=', rec.id)])
                new_folder_id = self.env['project.project'].browse(vals.get('project_id'))._get_document_folder()
                task_documents.write({'folder_id': new_folder_id.id})
        res = super(ProjectTask, self).write(vals)
        return res
    
    def _get_document_folder(self):
        if self.project_id.is_workspace:    
            return self.project_id.workspace_id
        else:
            return super(ProjectTask,self)._get_document_folder()
    
    def _check_create_documents(self):
        if self.project_id.is_workspace:    
            return self.project_id.workspace_id and super()._check_create_documents()
        else:
            return super(ProjectTask,self)._check_create_documents()


class DD(models.Model):
    _inherit = 'documents.document'

    def write(self, vals):
        for rec in self:
            if (vals.get('folder_id') and vals.get('folder_id') != rec.folder_id.id) and (
                    rec.res_model == 'project.project' or rec.res_model == 'project.task'):
                new_folder = self.env['documents.folder'].search([('id','=',vals.get('folder_id'))])
                if rec.folder_id.parent_folder_id:
                    previous_parent_folder_name = "%s/" % rec.folder_id.parent_folder_id.name
                    previous_folder_name = " ".join((previous_parent_folder_name, rec.folder_id.name))
                else:
                    previous_folder_name = rec.folder_id.name
                
                if new_folder.parent_folder_id:
                    new_folder_parent_name = "%s/" % new_folder.parent_folder_id.name
                    new_folder_name = " ".join((new_folder_parent_name, new_folder.name))
                else:
                    new_folder_name = new_folder.name
                body = """ <div>Document:  %s </div>
                
                          Workspace: 
                          %s  <div role="img" class="fa fa-long-arrow-right"></div>  %s
                          
                           """ % (rec.name, previous_folder_name, new_folder_name)
                self.env[rec.res_model].browse(rec.res_id).message_post(body=body)
        res = super(DD, self).write(vals)
        return res