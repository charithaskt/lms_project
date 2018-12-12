'use strict';

App.ko.ReserveGridRow = function(options) {
    $.inherit(App.ko.GridRow.prototype, this);
    this.init(options);
};

(function(ReserveGridRow) {

    ReserveGridRow.useInitClient = true;

    ReserveGridRow.toDisplayValue = function(value, field) {
        var displayValue = this._super._call('toDisplayValue', value, field);
        switch (field) {
        case 'category':
            // Display field value as bootstrap label.
            var types = ['success', 'info', 'primary'];
            displayValue = $('<span>', {
                'class': 'label preformatted'
            })
            .text(displayValue)
            .addClass(
                'label-' + (this.values[field] < types.length ? types[this.values[field]] : 'info')
            );
            break;
        case 'is_active':
            // Display field value as form input.
            var attrs = {
                'type': 'checkbox',
                'class': 'form-field biblio-reserve',
                'data-pkval': this.getValue(this.ownerGrid.meta.pkField),
                'name': field + '[]',
            };
            if (this.values[field]) {
                attrs['checked'] = 'checked';
            }
            displayValue = $('<input>', attrs);
        }
        return displayValue;
    };

    ReserveGridRow.hasEnabledAction = function(action) {
        if (action.name === 'quick_activate' && this.values['is_active'] === true) {
            return false;
        }
        if (action.name === 'quick_deactivate' && this.values['is_active'] === false) {
            return false;
        }
        return true;
    };

})(App.ko.ReserveGridRow.prototype);


App.ReserveGridActions = function(options) {
    $.inherit(App.GridActions.prototype, this);
    $.inherit(App.Actions.prototype, this);
    this.init(options);
};

(function(ReserveGridActions) {

    // Generates data for AJAX call.
    ReserveGridActions.queryargs_activate_reserves = function(options) {
        options['reserve_ids'] = JSON.stringify(this.grid.getActivatedReserveIds());
        return options;
    };

    ReserveGridActions.callback_endorse_reserves = function(viewModel) {
        this.grid.updatePage(viewModel);
        if (viewModel.update_rows.length > 0) {
            var vm = {
                title: 'Changed reserve activation status',
                description: viewModel.description
            };
            this.renderDescription(vm);
        } else {
            var vm = {
                'title': 'No reserve was changed',
                'message': 'Please invert some checkbox first.'
            };
        }
        // this.grid.updateMeta(viewModel.meta);
        new App.Dialog(vm).alert();
    };

    ReserveGridActions.callback_quick_endorse = function(viewModel) {
        this.grid.updatePage(viewModel);
    };

    ReserveGridActions.callback_quick_deactivate = function(viewModel) {
        this.grid.updatePage(viewModel);
    };
    """
    // Client-side invocation of the action.
    ReserveGridActions.perform_edit_note = function(queryArgs, ajaxCallback) {
        var actionDialog = new App.ActionTemplateDialog({
            template: 'reserve_note_form',
            owner: this.grid,
            meta: {
                noteLabel: 'Reserve note',
                note: this.grid.lastClickedKoRow.getValue('note')
            },
        });
        actionDialog.show();
    };
    """
    ReserveGridActions.callback_edit_note = function(viewModel) {
        this.grid.updatePage(viewModel);
    };

})(App.ReserveGridActions.prototype);


App.ko.ReserveGrid = function(options) {
    $.inherit(App.ko.Grid.prototype, this);
    this.init(options);
};

(function(ReserveGrid) {

    ReserveGrid.iocRow = function(options) {
        return new App.ko.ReserveGridRow(options);
    };

    ReserveGrid.iocGridActions = function(options) {
        return new App.ReserveGridActions(options);
    };

    ReserveGrid.getActiveReserveIds = function() {
        var reserves = {};
        $('input.biblio-reserve[name^="is_active"]')
        .map(function() {
            reserves[$(this).data('pkval')] = $(this).prop('checked');
        });
        return reserves;
    };

    ReserveGrid.onChangeActivation = function(data, ev) {
        this.actions.perform('activate_reserves');
    };

})(App.ko.ReserveGrid.prototype);
