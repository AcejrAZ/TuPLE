from traits.api import HasTraits, Float, Enum, on_trait_change
from traitsui.api import View, VGroup, HGroup, Item


class slices_example(HasTraits):
    number = Enum(1, 3, 5, 7, 9, 11, 13, 15)
    interval = Enum(0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)
    zrange = Float
    
    def __init__(self):
        super(slices_example, self).__init__()
    
    view = View(
      VGroup(
       HGroup(
        VGroup(
          Item(label='Number of Slices'),
          Item('number', show_label=False, width=0.25)),
        VGroup(
          Item(label='Interval (micron)'),
          Item('interval', show_label=False, width=0.25)),
        VGroup(
          Item(label='Z-Range (micron)'),
          Item('zrange', style='readonly', 
               show_label=False, width=0.25))
        )
       ),
      title='Edit slice properties',
      buttons=['OK', 'Cancel'])

    @on_trait_change('number, interval')
    def _zrange_update(self):
        self.zrange = ( self.number - 1 ) * self.interval

if __name__ == '__main__':
    dialog = slices_example()
    dialog.configure_traits()
