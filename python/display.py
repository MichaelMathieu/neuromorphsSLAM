import gtk, gtk.gdk, cairo
import math

class Canvas(gtk.DrawingArea):
    def __init__(self, surface, w, h):
        super(Canvas, self).__init__()
        self.connect("expose_event", self.expose)
        self.set_size_request(w, h)
        self.surface = surface
    
    def expose(self, widget, event):
        #TODO: subobtimal, but it is not the point
        cr = widget.window.cairo_create()
        cr.set_source_surface(self.surface,0,0)
        cr.paint()

class GUI(object):
    def __init__(self, scale = 1, wpixels = 100, hpixels = 100,
                 xoffset = 0, yoffset = 0):
        self.wpixels = int(math.ceil(wpixels))
        self.hpixels = int(math.ceil(hpixels))
        self.create_window()
        self.scale = scale
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.main_window.connect("key-press-event", self.on_key_pressed)
        self.main_window.connect("key-release-event", self.on_key_released)
        self.keyboard_state = {}

    def save(self, filename):
        self.surface.write_to_png(filename)

    def create_window(self):
        self.main_window = gtk.Window(type=gtk.WINDOW_TOPLEVEL)
        self.main_window.connect("destroy", self.main_quit)
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                          self.wpixels, self.hpixels)
        self.draw_context = cairo.Context(self.surface)
        self.draw_context.set_source_rgb(1, 1, 1)
        self.draw_context.set_operator(cairo.OPERATOR_SOURCE)
        self.draw_context.paint()
        self.draw_context.set_operator(cairo.OPERATOR_OVER)
        self.draw_context.set_line_join(cairo.LINE_JOIN_ROUND)
        self.draw_context.set_line_cap(cairo.LINE_CAP_ROUND)
        self.line_width = 2
        self.draw_context.set_line_width(self.line_width)
        self.canvas = Canvas(self.surface, self.wpixels, self.hpixels)
        self.main_window.add(self.canvas)
        self.main_window.show_all()

    def on_key_pressed(self, window, event):
        if window == self.main_window:
            keyname = gtk.gdk.keyval_name(event.keyval)
            self.keyboard_state[keyname] = True

    def on_key_released(self, window, event):
        if window == self.main_window:
            keyname = gtk.gdk.keyval_name(event.keyval)
            self.keyboard_state[keyname] = False

    def main_quit(self, *args):
        exit(0)

    def keyState(self, key):
        # key can be a letter or "Up", "Down", "Left", "Right", "space"
        # see gtk.gdk.keyval_name documentation for the other keys
        if key not in self.keyboard_state:
            return False
        else:
            return self.keyboard_state[key]
        

    def erase(self):
        self.draw_context.set_source_rgb(1, 1, 1)
        self.draw_context.set_operator(cairo.OPERATOR_SOURCE)
        self.draw_context.paint()
        self.canvas.queue_draw()
    
    def line(self, x1_, y1_, x2_, y2_, color = (0,0,0), width = None):
        x1 = float(x1_)*self.scale + self.xoffset
        x2 = float(x2_)*self.scale + self.xoffset
        y1 = float(y1_)*self.scale + self.yoffset
        y2 = float(y2_)*self.scale + self.yoffset
        if width == None:
            width = self.line_width
        self.draw_context.set_line_width(width)
        if len(color) == 3:
            self.draw_context.set_source_rgb(*color)
        else:
            self.draw_context.set_source_rgba(*color)
        self.draw_context.set_operator(cairo.OPERATOR_SOURCE)
        self.draw_context.move_to(x1, y1)
        self.draw_context.line_to(x2, y2)
        self.draw_context.stroke()
        x1_ = int(math.floor(min(x1, x2)))
        x2_ = int(math.ceil(max(x1, x2)))
        y1_ = int(math.floor(min(y1, y2)))
        y2_ = int(math.ceil(max(y1, y2)))
        self.canvas.queue_draw_area(int(math.floor(x1_ - width)),
                                    int(math.floor(y1_ - width)),
                                    int(math.ceil(x2_ - x1_ + 2*width)) + 2,
                                    int(math.ceil(y2_ - y1_ + 2*width)) + 2)

    def oriented_line(self, x1, y1, x2, y2, color = (0,0,0), width = None):
        if width == None:
            width = self.line_width
        self.line(x1, y1, x2, y2, color, width)
        xmid = 0.5*(x1+x2)
        ymid = 0.5*(y1+y2)
        
        xn = x2-x1
        yn = y2-y1
        nn = math.sqrt(xn*xn+yn*yn)
        xn *= width/nn*0.75
        yn *= width/nn*0.75
        self.line(xmid+yn-xn, ymid-xn-yn, xmid, ymid, color, width)
        self.line(xmid-yn-xn, ymid+xn-yn, xmid, ymid, color, width)
        
    def point(self, x_, y_, color=(1,0,0), width = None):
        x = x_*self.scale + self.xoffset
        y = y_*self.scale + self.yoffset
        if len(color) == 3:
            self.draw_context.set_source_rgb(*color)
        else:
            self.draw_context.set_source_rgba(*color)
        self.draw_context.new_path()
        if width == None:
            width = self.line_width
        self.draw_context.arc(x, y, width, 0, 2 * math.pi)
        self.draw_context.fill()
        self.canvas.queue_draw_area(int(math.floor(x)) - width,
                                    int(math.floor(y)) - width,
                                    2 * width+2,
                                    2 * width+2)

