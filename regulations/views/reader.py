from django.views.generic.base import (
    TemplateView,
    View,
)
from django.http import Http404
from django.urls import reverse
from django.http import HttpResponseRedirect

from regulations.generator import api_reader
from regulations.views import utils
from regulations.views.mixins import SidebarContextMixin, CitationContextMixin, TableOfContentsMixin
from regulations.views.utils import find_subpart


class ReaderView(TableOfContentsMixin, SidebarContextMixin, CitationContextMixin, TemplateView):

    template_name = 'regulations/reader.html'

    sectional_links = True

    client = api_reader.ApiReader()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # getting url info (label and version)
        # answering the question: what are we looking at?
        reg_version = context["version"]
        reg_part = context["part"]
        reg_citation = context["citation"]
        toc = self.get_toc(reg_part, reg_version)
        meta = utils.regulation_meta(reg_part, reg_version)
        tree = self.get_regulation(reg_citation, reg_version)

        if not meta:
            raise Http404

        c = {
            'tree':         tree,
            'reg_part':     reg_part,
            'meta':         meta,
            'TOC':          toc,
        }

        links = self.get_view_links(context, toc)

        return {**context, **c, **links}

    def get_regulation(self, label_id, version):
        regulation = self.client.regulation(label_id, version)
        if regulation is None:
            raise Http404
        return regulation

    def get_view_links(self, context, toc):
        raise NotImplementedError()


class PartReaderView(ReaderView):
    def get_view_links(self, context, toc):
        part = context['part']
        version = context['version']
        first_section = utils.first_section(part, version)
        first_subpart = utils.first_subpart(part, version)

        return {
            'subpart_view_link': reverse('reader_view', args=(part, first_subpart, version)),
            'section_view_link': reverse('reader_view', args=(part, first_section, version)),
        }

    def build_toc_url(self, part, subpart, section, version):
        return reverse('reader_view', args=(part, version))


class SubpartReaderView(ReaderView):
    def get_view_links(self, context, toc):
        part = context['part']
        version = context['version']
        subpart = context['subpart']
        section = utils.find_subpart_first_section(subpart, toc)
        if section is None:
            section = utils.first_section(part, version)
        citation = part + '-' + section

        return {
            'part_view_link': reverse('reader_view', args=(part, version)) + '#' + citation,
            'section_view_link': reverse('reader_view', args=(part, section, version)),
        }


class SectionReaderView(TableOfContentsMixin, View):
    def get(self, request, *args, **kwargs):
        url_kwargs = {
            "part": kwargs.get("part"),
            "version": kwargs.get("version"),
        }

        toc = self.get_toc(kwargs.get("part"), kwargs.get("version"))
        subpart = find_subpart(kwargs.get("section"), toc)
        if subpart is not None:
            url_kwargs["subpart"] = subpart

        url = reverse("reader_view", kwargs=url_kwargs)
        return HttpResponseRedirect(url)