'use strict';

App.ko.HoldGridRow = function(options) {
    $.inherit(App.ko.GridRow.prototype, this);
    this.init(options);
};

(function(HoldGridRow) {

    HoldGridRow.useInitClient = true;

    HoldGridRow.toDisplayValue = function(value, field) {
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

    HoldGridRow.hasEnabledAction = function(action) {
        if (action.name === 'quick_activate' && this.values['is_active'] === true) {
            return false;
        }
        if (action.name === 'quick_deactivate' && this.values['is_active'] === false) {
            return false;
        }
        return true;
    };

})(App.ko.HoldGridRow.prototype);


App.HoldGridActions = function(options) {
    $.inherit(App.GridActions.prototype, this);
    $.inherit(App.Actions.prototype, this);
    this.init(options);
};

(function(HoldGridActions) {

    // Generates data for AJAX call.
    HoldGridActions.queryargs_activate_holds = function(options) {
        options['reserve_ids'] = JSON.stringify(this.grid.getActivatedHoldIds());
        return options;
    };

    HoldGridActions.callback_endorse_holds = function(viewModel) {
        this.grid.updatePage(viewModel);
        if (viewModel.update_rows.length > 0) {
            var vm = {
                title: 'Changed hold activation status',
                description: viewModel.description
            };
            this.renderDescription(vm);
        } else {
            var vm = {
                'title': 'No hold was changed',
                'message': 'Please invert some checkbox first.'
            };
        }
        // this.grid.updateMeta(viewModel.meta);
        new App.Dialog(vm).alert();
    };

    HoldGridActions.callback_quick_endorse = function(viewModel) {
        this.grid.updatePage(viewModel);
    };

    HoldGridActions.callback_quick_deactivate = function(viewModel) {
        this.grid.updatePage(viewModel);
    };
    """
    // Client-side invocation of the action.
    HoldGridActions.perform_edit_note = function(queryArgs, ajaxCallback) {
        var actionDialog = new App.ActionTemplateDialog({
            template: 'hold_note_form',
            owner: this.grid,
            meta: {
                noteLabel: 'Hold note',
                note: this.grid.lastClickedKoRow.getValue('note')
            },
        });
        actionDialog.show();
    };
    """
    HoldGridActions.callback_edit_note = function(viewModel) {
        this.grid.updatePage(viewModel);
    };

})(App.HoldGridActions.prototype);


App.ko.HoldGrid = function(options) {
    $.inherit(App.ko.Grid.prototype, this);
    this.init(options);
};

(function(HoldGrid) {

    HoldGrid.iocRow = function(options) {
        return new App.ko.HoldGridRow(options);
    };

    HoldGrid.iocGridActions = function(options) {
        return new App.HoldGridActions(options);
    };

    HoldGrid.getActiveHoldIds = function() {
        var reserves = {};
        $('input.biblio-hold[name^="is_active"]')
        .map(function() {
            holds[$(this).data('pkval')] = $(this).prop('checked');
        });
        return holds;
    };

    HoldGrid.onChangeActivation = function(data, ev) {
        this.actions.perform('activate_holds');
    };

})(App.ko.HoldGrid.prototype);
