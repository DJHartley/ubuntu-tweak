import os
import gtk
import sys
import pango
import gobject

from common.consts import DATA_DIR
from tweak.utils import icon

class TweakModule(gtk.VBox):
    __name__ = ''
    __version__ = ''
    __icon__ = ''
    __author__ = ''
    __desc__ = ''
    __url__ = ''

    __gsignals__ = {
            'update': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING, gobject.TYPE_STRING)),
            'call': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)),
    }

    def __init__(self, path=None, domain='ubuntu-tweak'):
        assert(self.__name__ and self.__desc__)

        gtk.VBox.__init__(self)

        self.draw_title()

        self.inner_vbox = gtk.VBox(False, 6)
        self.pack_start(self.inner_vbox, False, False, 0)

        if path:
            path = os.path.join(DATA_DIR, 'gui', path)

            self.builder = gtk.Builder()
            self.builder.set_translation_domain(domain)
            self.builder.add_from_file(path)
            self.builder.connect_signals(self)
            for o in self.builder.get_objects():
                if issubclass(type(o), gtk.Buildable):
                    name = gtk.Buildable.get_name(o)
                    setattr(self, name, o)
                else:
                    print >>sys.stderr, "WARNING: can not get name for '%s'" % o
            self.reparent()
        else:
            self.inner_vbox.set_border_width(5)

    def add_start(self, child, expand=True, fill=True, padding=0):
        self.inner_vbox.pack_start(child, expand, fill, padding)

    def add_end(self, child, expand=True, fill=True, padding=0):
        self.inner_vbox.pack_end(child, expand, fill, padding)

    def draw_title(self):
        eventbox = gtk.EventBox()
        eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
        self.pack_start(eventbox, False, False, 0)

        vbox = gtk.VBox()
        eventbox.add(vbox)

        align = gtk.Alignment(0.5, 0.5, 1.0, 1.0)
        align.set_padding(5, 5, 5, 5)
        vbox.pack_start(align)

        hbox = gtk.HBox(False, 6)
        align.add(hbox)

        inner_vbox = gtk.VBox(False, 6)
        hbox.pack_start(inner_vbox)

        name = gtk.Label()
        name.set_markup('<b><big>%s</big></b>' % self.__name__)
        name.set_alignment(0, 0.5)
        inner_vbox.pack_start(name, False, False, 0)

        if self.__url__:
            align = gtk.Alignment(0.5, 0.5, 1.0, 1.0)
            inner_vbox.pack_start(align)

            inner_hbox = gtk.HBox(False, 0)
            align.add(inner_hbox)

            left_box = gtk.VBox(False, 6)
            inner_hbox.pack_start(left_box)

            right_box = gtk.VBox(False, 6)
            inner_hbox.pack_start(right_box, False, False, 0)

            desc = gtk.Label(self.__desc__)
            desc.set_ellipsize(pango.ELLIPSIZE_END)
            desc.set_alignment(0, 1)
            left_box.pack_start(desc, False, False, 0)

            more = gtk.Label()
            more.set_markup('<a href="%s">%s</a>' % (self.__url__, 'More'))
            right_box.pack_start(more, False, False, 0)
        else:
            desc = gtk.Label(self.__desc__)
            desc.set_ellipsize(pango.ELLIPSIZE_END)
            desc.set_alignment(0, 0.5)
            inner_vbox.pack_start(desc, False, False, 0)

        if self.__icon__:
            if self.__icon__.endswith('.png'):
                icon_path = os.path.join(DATA_DIR, 'pixmaps', self.__icon__)
                image = gtk.image_new_from_file(icon_path)
            else:
                pixbuf = icon.get_with_name(self.__icon__, size=48)
                image = gtk.image_new_from_pixbuf(pixbuf)
            hbox.pack_end(image, False, False, 0)

        vbox.pack_start(gtk.HSeparator(), False, False, 0)

    def reparent(self):
        raise NotImplementedError
