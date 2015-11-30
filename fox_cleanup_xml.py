import sublime, sublime_plugin

import re

class foxCleanupXmlCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.settings().set('syntax', 'Packages/XML/XML.tmLanguage')
    self._edit = edit
    if (self._is_SFD()):
      self._clean_for_sfd();
    self._replace_all(r" xmlns=\"[\S]*?\"", "")
    # test comment changed again, now this should end up in version 1.0.3
    self.view.run_command("indentxml")

  def _get_file_content(self):
    return self.view.substr(sublime.Region(0, self.view.size()))

  def _is_SFD(self):
    return '--MIME_boundary' in self._get_file_content()

  def _clean_for_sfd(self):
    startpos = self._get_file_content().find('<?xml ')
    self.view.erase(self._edit, sublime.Region(0, startpos))
    endpos = self._get_file_content().find('--MIME_boundary', startpos)
    self.view.erase(self._edit, sublime.Region(endpos, self.view.size()))

  def _update_file(self, doc):
    self.view.replace(self._edit, sublime.Region(0, self.view.size()), doc)

  def _replace_all(self, regex, replacement):
    doc = self._get_file_content()
    p = re.compile(regex, re.UNICODE)
    doc = re.sub(p, replacement, doc)
    self._update_file(doc)