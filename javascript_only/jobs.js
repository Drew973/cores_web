//http://127.0.0.1:8000/static/jobs.html



addJobText = 'Add new job...';
token = '';

function setForm(form, data) {
	//console.log('setForm',data)	
    const entries = (new URLSearchParams(data)).entries();
    for(const [key, val] of entries) {
        //http://javascript-coder.com/javascript-form/javascript-form-value.phtml
        const input = form.elements[key];
        switch(input.type) {
            case 'checkbox': input.checked = !!val; break;
            default:         input.value = val;     break;
        }
    }
}



async function updateJob()
{
	var jn = getJobNumber();
	const formData = new FormData(document.getElementById("job_form"));
	try {
		const response = await fetch("/update_job/"+jn, {method: "POST",body: formData,});
		console.log(await response);
		updateJobs();
		} 
	catch (e){
		console.error(e);
		}
		update_job_form();
}


async function submitJob(){
	var jn = getJobNumber();	
	if (jn == addJobText){
		addJob();
		console.log('add job');
		}
	else {updateJob();}
	}



async function delete_job_handler()
	{
	var jn = getJobNumber();
	if (confirm('Delete job "'+jn+'" and any cores with this job_number?')) 
	{
		fetch('/delete_job/'+jn,{method: 'delete'})
		.then(response => response.json())
		.then(data => {
			console.log(data);
			console.log('deleted job');
			updateJobs();
			}
			)
	.catch(error => console.error(error));
	}}


async function update_job_form(){
	job_number = getJobNumber();
	if (job_number == addJobText){
		document.getElementById("job_form").reset();
		document.getElementById("jobLegend").innerHTML = addJobText;
		document.getElementById("submitButton").innerHTML = 'Add';
		return;
	}
//	console.log('update_job_form:'+job_number);



fetch("/get_job_details?job_number="+job_number, {
  headers:
  {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
    }
})
	.then(response => response.json())
	.then(data => 
		{//console.log(data);
		setForm(document.getElementById("job_form"),data);
		document.getElementById("jobLegend").innerHTML = 'Edit: '+data.job_number;
		document.getElementById("submitButton").innerHTML = 'Submit changes';
		})
	.catch(error => console.error(error));
	}
		

//sets options of select element sel to values. Then sets to default_opt if exists.
function set_options(sel,values,default_opt){
	arrOptions = [];
	values.forEach((v) => arrOptions.push("<option>" + v + "</option>"))
	sel.innerHTML = arrOptions.join();
	i = values.indexOf(default_opt);
	sel.value = default_opt;
	//console.log('selected ind:'+i);
	return i;
}


function jobChanged(){
	jn = getJobNumber();
	setJobNumber(jn);
}


function setJobNumber(job){
	//set url query parameter
	const url = new URL(window.location.href);
	url.searchParams.set('job_number', job);
	window.history.pushState(null, '', url.toString());
	//set select
	e = document.getElementById("jobSelect");
	e.value = job;
	update_job_form();
}
	

function getJobNumber(){
	return document.getElementById("jobSelect").value;
}


//update options of job number select
async function updateJobs()
{
	cur = getJobNumber();
	var s = document.getElementById("jobSelect");
	fetch("/get_job_numbers")
	.then(response => response.json())
	.then(data => 
		{
	//	console.log(data);
		set_options(s,[addJobText].concat(data),cur);
		setJobFromUrl();
		})
	.catch(error => {
		console.error(error);		
		setJobFromUrl()});
}


//submit changes to database
async function addJob(){
	const formData = new FormData(document.getElementById("job_form"));
//	console.log('add job');
	//console.log(formData);
	fetch("/add_job/", {method: "POST",body: formData,})
	.then(response => response.json())
	.then(data => 
		{
			console.log(data);
			setJobNumber(data.job_number);
		})
	.catch(error => {
		console.error(error);
		alert(error);
		})
	}



function addJobButtonHandler(){
	setJobNumber(addJobText);
	update_job_form();
}

function setJobFromUrl(){
	const urlParams = new URLSearchParams(window.location.search);
	const current = urlParams.get('job_number');
	setJobNumber(current);
}



const loginForm = document.getElementById('loginForm'); 
loginForm.addEventListener('submit', function(event) { 
  event.preventDefault(); 
  submitLogin();
}); 



function submitLogin(){
	token = '';
	const formData = new FormData(document.getElementById("loginForm"));
	fetch("/login/", {method: "POST",body: formData,})
	.then(response => response.json())
	.then(data => 
		{
			console.log(data);
			token = data;
		})
	.catch(error => {
		console.error(error);
		alert(error);
		})
		
	}