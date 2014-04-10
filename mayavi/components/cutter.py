"""A simple wrapper for `tvtk.Cutter`.
"""
# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2005-2008, Enthought, Inc.
# License: BSD Style.


# Enthought library imports.
from traits.api import Instance, Property
from traitsui.api import View, Group, Item
from tvtk.api import tvtk

# Local imports.
from mayavi.core.component import Component
from mayavi.core.common import is_old_pipeline


######################################################################
# `Cutter` class.
######################################################################
class Cutter(Component):
    # The version of this class.  Used for persistence.
    __version__ = 0

    # The mapper.
    cutter = Instance(tvtk.Cutter, args=())

    # The cut function.  This should be a delegate but due to a bug in
    # traits that does not work.
    cut_function = Property

    ########################################
    # View related traits.

    view = View(Group(Item(name='cutter',
                           style='custom',
                           resizable=True),
                      show_labels=False),
                resizable=True)

    ######################################################################
    # `Component` interface
    ######################################################################
    def update_pipeline(self):
        """Override this method so that it *updates* the tvtk pipeline
        when data upstream is known to have changed.

        This method is invoked (automatically) when the input fires a
        `pipeline_changed` event.
        """
        if (len(self.inputs) == 0) or (len(self.inputs[0].outputs) == 0):
            return
        c = self.cutter
        self.configure_connection(c, self.inputs[0])
        self.outputs = [c.output]

    def update_data(self):
        """Override this method to do what is necessary when upstream
        data changes.

        This method is invoked (automatically) when any of the inputs
        sends a `data_changed` event.
        """
        self.data_changed = True

    def has_output_port(self):
        """ The contour filter has an output port."""
        return True

    def get_output_object(self):
        """ Returns the output port."""
        return self.cutter.output_port

    ######################################################################
    # `Cutter` interface
    ######################################################################
    def _get_cut_function(self):
        return self.cutter.cut_function

    def _set_cut_function(self, val):
        old = self.cutter.cut_function
        self.cutter.cut_function = val
        self.trait_property_changed('cut_function', old, val)

