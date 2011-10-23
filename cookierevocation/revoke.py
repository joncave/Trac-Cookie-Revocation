# -*- coding: utf-8 -*-
#
# CookieRevocation - a short Trac plugin to enable the revocation
# of a user's trac_auth cookie.

from pkg_resources   import resource_filename

from trac.core       import *
from trac.admin      import IAdminPanelProvider
from trac.web.chrome import ITemplateProvider, add_notice, add_warning
from trac.util.text  import exception_to_unicode

class CookieRevocation(Component):

    implements(IAdminPanelProvider, ITemplateProvider)

    # IAdminPanelProvider methods

    def get_admin_panels(self, req):
        """Add the CookieRevocation admin panel"""
        if 'TRAC_ADMIN' in req.perm:
            yield ('general', 'General', 'revoke-cookie', 'Revoke A Cookie')

    def render_admin_panel(self, req, cat, page, version):
        """Render the CookieRevocation admin panel and handle POST requests to
        delete a user's trac_auth cookie from the auth_cookie table.
        """
        req.perm.require('TRAC_ADMIN')
        if req.method == 'POST':
            user = req.args.get('user')
            if user:
                @self.env.with_transaction()
                def revoke_auth_cookie(db):
                    cursor = db.cursor()
                    cursor.execute("DELETE FROM auth_cookie WHERE name = %s", (user,))
                self.log.info('Cookie revoked for user %s', user)
                add_notice(req, 'Cookie revoked!')
            else:
                add_warning(req, 'You did not provide a username')
        return 'revoke.html', {}

    # ITemplateProvider methods

    def get_htdocs_dirs(self):
        """Return the absolute path of a directory containing additional
        static resources (such as images, style sheets, etc).
        """
        return []

    def get_templates_dirs(self):
        """Return the absolute path of the directory containing the provided
        Genshi templates.
        """
        return [resource_filename(__name__, 'templates')]
