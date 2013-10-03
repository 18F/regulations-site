define('main-view', ['jquery', 'underscore', 'backbone', 'dispatch', 'search-results-view', 'reg-view', 'reg-model', 'search-model', 'sub-head-view'], function($, _, Backbone, Dispatch, SearchResultsView, RegView, RegModel, SearchModel, SubHeadView) {
    'use strict';

    var MainView = Backbone.View.extend({
        el: '#content-body',

        initialize: function() {
            this.header = new SubHeadView();

            Dispatch.on('mainContent:change', this.render, this);
            Dispatch.on('regSection:open', this.loadContent, this);
            Dispatch.on('search:submitted', this.assembleSearchURL, this);
        },

        modelmap: {
            'regSection': RegModel,
            'searchResults': SearchModel
        }, 

        viewmap: {
            'regSection': RegView,
            'searchResults': SearchResultsView
        },

        assembleSearchURL: function(options, type) {
            var url = Dispatch.getRegId();
            url += '?q=' + options.query;
            url += '&version=' + options.version;

            if (typeof options.page !== 'undefined') {
                url += '&page=' + options.page;
            }

            options.url = url;
            this.loadContent(url, options, type);
        },

        loadContent: function(getParam, options, type) {
            this.loading();
            var returned = this.modelmap[type].get(getParam);

            if (typeof returned.done !== 'undefined') {
                // @TODO: error handling
                returned.done(function(response) {
                    this.createView(response, options, type);
                }.bind(this));

                returned.fail(function() {
                    var alertNode = document.createElement('div');

                    alertNode.innerHTML = 'There was an issue loading your data. This may be because your device is currently offline. Please try again.';
                    alertNode.className = 'alert';

                    $(alertNode).insertBefore('h2.section-number');
                    this.loaded();
                }.bind(this));
            }
            else {
               this.createView(returned, options, type); 
            }
        },

        createView: function(html, options, type) {
            Dispatch.removeContentView();
            this.render(html, options.scrollToId);
            Dispatch.setContentView(new this.viewmap[type](options));
            this.loaded();
        },

        render: function(html, scrollToId) {
            var offsetTop, $scrollToId;

            this.header.reset();
            this.$el.html(html);

            if (typeof scrollToId !== 'undefined') {
                $scrollToId = $('#' + scrollToId);
                if ($scrollToId.length > 0) {
                    offsetTop = $scrollToId.offset().top;
                }
            }

            window.scrollTo(0, offsetTop || 0);
        },

        loading: function() {
            // visually indicate that a new section is loading
            $('.main-content').addClass('loading');

        },

        loaded: function() {
            $('.main-content').removeClass('loading');

            // change focus to main content area when new sections are loaded
            $('.section-focus').focus();
        }
    });

    return MainView;
});
