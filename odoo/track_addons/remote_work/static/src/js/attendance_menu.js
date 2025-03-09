odoo.define('remote_work.attendance_menu', function (require) {
    "use strict";

    const { Component } = require('owl');
    const { useState } = require('react');

    // Define the component for attendance menu extension
    class AttendanceMenuExtension extends Component {
        constructor() {
            super(...arguments);
            this.state = useState({
                checkedIn: false, // This will store the checked-in state
                isDisplayed: true, // This will determine if the menu is displayed
            });
        }

        // Function to handle the "Take Pause" button click
        onClickTakePause() {
            console.log("Take Pause button clicked!");
            // Add any logic here for the pause functionality
            // For example, you can update the state or make an API call to mark the pause
            this.state.checkedIn = false; // Update checked-in status or handle pause
        }

        render() {
            return (
                <div class="attendance-menu-extension">
                    <button
                        t-on-click="() => this.onClickTakePause()"
                        class="btn btn-info flex-basis-100 mt-2">
                        <span class="align-middle fs-2 me-3 text-white">Take Pause</span>
                        <i class="fa fa-coffee fa-2x align-middle"/>
                    </button>
                </div>
            );
        }
    }

    // Add the component to the Owl registry
    const AttendanceMenuComponent = new AttendanceMenuExtension();
    AttendanceMenuComponent.mount('#attendance-menu');
});
