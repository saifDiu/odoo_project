# -*- coding: utf-8 -*-
{
  "name":  "WT Backend Debrand",
  "summary":  "backend debranding module.",
  "category":  "web",
  "version":  "1.0.1",
  "sequence":  1,
  "author":  "warlocktechnologies",
  "license":  "Other proprietary",
  "website":  "https://www.warlocktechnologies.com/",
  "description":  "backend debranding module.",
  "depends":  ['base_setup', 'web', 'iap', 'mail'],
  "data": [
            'data/data.xml',
            'views/views.xml',
            'views/template.xml'
          ],
  'qweb': [
        'static/src/xml/backend.xml',
  ],
  "installable":  True,
  "auto_install":  True,
}