import { Calendar, DateSelectArg, EventDropArg, EventChangeArg, EventClickArg } from '@fullcalendar/core';

import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

function setupCalendar(): void {
	const elem = document.getElementById('calendar');
	if (!elem)
		return;
	const calendar = new Calendar(elem, {
		plugins: [timeGridPlugin, interactionPlugin],
		initialView: 'timeGridWeek',

		headerToolbar: false,
		allDaySlot: false,
		firstDay: 1,
		dayHeaderFormat: { weekday: 'long' },
		slotMinTime: '06:00:00',
		slotMaxTime: '21:00:00',
		slotDuration: '00:30:00',
		slotLabelFormat: { hour: '2-digit', minute: '2-digit', hour12: false },
		eventTimeFormat: { hour: '2-digit', minute: '2-digit', hour12: false },

		selectable: true,				// allows selecting time ranges to create events
		editable: true,					// allows drag & drop and resizing
		selectMirror: true,				// shows a temporary event while dragging
		weekends: false,

		select: function(info: DateSelectArg): void {
			// triggered when user selects a time slot
			calendar.addEvent({
				title: '',
				start: info.start,
				end: info.end,
				allDay: info.allDay
			});
			calendar.unselect();
		},

		eventDrop: function(info: EventDropArg): void {
			// triggered when user drags an event to a new time
			console.log('Event moved to:', info.event.start, info.event.end);
			// Here you can call your Fastify API to save changes
		},

		eventResize: function(info: EventChangeArg): void {
			console.log('Event resized to:', info.event.start, info.event.end);
		},

		eventClick: function(info: EventClickArg): void {
			info.event.remove();
		},
	});

	calendar.render();
}

export { setupCalendar };
