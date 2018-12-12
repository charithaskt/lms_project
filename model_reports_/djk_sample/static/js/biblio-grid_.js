/**
 * This code is partially shared between these templates / class-based views
 *
 * 'biblio_grid_with_action_logging.htm' / ils_app.views_ajax.BiblioGridWithActionLogging
 * 'biblio_item.htm' / ils_app.views_ajax.BiblioItemGrid
 *
 */
App.BiblioGridActions = function(options) {
    $.inherit(App.GridActions.prototype, this);
    $.inherit(App.Actions.prototype, this);
    this.init(options);
};

(function(BiblioGridActions) {

    BiblioGridActions.updateDependentGrid = function(selector) {
        // Get instance of dependent grid.
        var grid = $(selector).component();
        if (grid !== null) {
            // Update dependent grid.
            grid.actions.perform('update');
        }
    };

    // Used in ils_app.views_ajax.BiblioGridWithActionLogging.
    BiblioGridActions.callback_save_inline = function(viewModel) {
        this._super._call('callback_save_form', viewModel);
        this.updateDependentGrid('#action_grid');
        this.updateDependentGrid('#item_grid');
    };

    // Used in ils_app.views_ajax.BiblioItemGrid.
    BiblioGridActions.callback_save_form = function(viewModel) {
        this._super._call('callback_save_form', viewModel);
        this.updateDependentGrid('#action_grid');
        this.updateDependentGrid('#item_grid');
    };

    BiblioGridActions.callback_delete_confirmed = function(viewModel) {
        this._super._call('callback_delete_confirmed', viewModel);
        this.updateDependentGrid('#action_grid');
        this.updateDependentGrid('#item_grid');
    };

    BiblioGridActions.callback_add_item = function(viewModel) {
        this.callback_create_form(viewModel);
    };

    BiblioGridActions.callback_save_item = function(viewModel) {
        var itemGridView = viewModel.item_grid_view;
        delete viewModel.item_grid_view;
        this.grid.updatePage(viewModel);
        // Get client-side class of ItemGrid component by id (instance of App.ko.Grid or derived class).
        var itemGrid = $('#item_grid').component();
        if (itemGrid !== null) {
            // Update rows of BiblioGrid component (instance of App.ko.Grid or derived class).
            itemGrid.updatePage(itemGridView);
            // Highlight item tab so the user will know it has updated list page.
            App.TabPane().highlight('#item_tab');
            // Switch to item grid tab to show item changes.
            // window.location.hash = '#item_tab';
        }
    };

})(App.BiblioGridActions.prototype);


App.ko.BiblioGrid = function(options) {
    $.inherit(App.ko.Grid.prototype, this);
    this.init(options);
};

(function(BiblioGrid) {

    BiblioGrid.iocGridActions = function(options) {
        return new App.BiblioGridActions(options);
    };

})(App.ko.BiblioGrid.prototype);
