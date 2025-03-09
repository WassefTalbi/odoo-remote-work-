odoo.define('remote_work.attendance_pause', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var Widget = require('web.Widget');

    publicWidget.registry.AttendanceMenu = Widget.extend({
        selector: '.o_att_menu_container',
        events: {
            'click .o_take_pause': '_onTakePause',
        },
        start: function () {
            this._super.apply(this, arguments);
            this.state = {
                isOnPause: false,
                checkedIn: false,  // Initially set to false
            };
        },
        _onTakePause: function () {
            // Toggle the pause state
            this.state.isOnPause = !this.state.isOnPause;
            this.render();
        },
        signInOut: function () {
            // Handle the Check-in/Check-out logic
            this.state.checkedIn = !this.state.checkedIn;
            this.render();
        },
        render: function () {
            // Re-render the widget to reflect the state changes
            this.$el.html(this._render());
        },
        _render: function () {
            return `
                <button t-on-click="() => this.signInOut()" class="flex-basis-100 mt-3" t-attf-class="btn btn-${this.state.checkedIn ? 'warning' : 'success'}">
                    <span t-if="!this.state.checkedIn">Check in</span>
                    <span t-else="">Check out</span>
                    <i class="fa fa-sign-${this.state.checkedIn ? 'out' : 'in'} ms-1"/>
                </button>
                <button t-if="this.state.checkedIn" class="o_take_pause flex-basis-100 mt-3" t-attf-class="btn btn-${this.state.isOnPause ? 'warning' : 'secondary'}">
                    ${this.state.isOnPause ? 'Resume' : 'Take Pause'}
                </button>
            `;
        },
    });
});
