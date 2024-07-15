const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

allSideMenu.forEach(item=> {
	const li = item.parentElement;

	item.addEventListener('click', function () {
		allSideMenu.forEach(i=> {
			i.parentElement.classList.remove('active');
		})
		li.classList.add('active');
	})
});




// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
	sidebar.classList.toggle('hide');
})







const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
	if(window.innerWidth < 576) {
		e.preventDefault();
		searchForm.classList.toggle('show');
		if(searchForm.classList.contains('show')) {
			searchButtonIcon.classList.replace('bx-search', 'bx-x');
		} else {
			searchButtonIcon.classList.replace('bx-x', 'bx-search');
		}
	}
})





if(window.innerWidth < 768) {
	sidebar.classList.add('hide');
} else if(window.innerWidth > 576) {
	searchButtonIcon.classList.replace('bx-x', 'bx-search');
	searchForm.classList.remove('show');
}


window.addEventListener('resize', function () {
	if(this.innerWidth > 576) {
		searchButtonIcon.classList.replace('bx-x', 'bx-search');
		searchForm.classList.remove('show');
	}
})



const switchMode = document.getElementById('switch-mode');

switchMode.addEventListener('change', function () {
	if(this.checked) {
		document.body.classList.add('dark');
	} else {
		document.body.classList.remove('dark');
	}
})

const fromDateInput = document.getElementById('from-date');
const toDateInput = document.getElementById('to-date');
const fromDateCalendar = document.getElementById('from-date-calendar');
const toDateCalendar = document.getElementById('to-date-calendar');
const leaveForm = document.getElementById('leave-form');

$(function() {
	$('from-date').datepicker();
	$('to-date').datepicker();
});

// Validate date range
function validateDateRange() {
  const fromDate = fromDateInput.value;
  const toDate = toDateInput.value;

  if (toDate < fromDate) {
    alert('Invalid date range. To date must be after from date.');
    toDateInput.value = '';
    toDateInput.focus();
  }
}

// Add event listener to form submit
leaveForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const leaveType = document.getElementById('leave-type').value;
  const leaveReason = document.getElementById('leave-reason').value;

  if (leaveType === '' || leaveReason === '') {
    alert('Please fill in all fields.');
  } else {
    // Submit form data to server
    console.log('Form submitted successfully!');
  }
});
