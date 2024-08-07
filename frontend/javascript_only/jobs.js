var host = "http://127.0.0.1:8000"
//http://127.0.0.1:8000/static/jobs.html?job_number=other_job



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



function get_job_number()
{
	return document.getElementById("job_select").value
}



async function update_job_handler()
{
	var jn = get_job_number();
	const formData = new FormData(document.getElementById("job_form"));
	try {
		const response = await fetch(host+"/update_job/"+jn, {method: "POST",body: formData,});
		console.log(await response);
		update_jobs();
		} 
	catch (e){
		console.error(e);
		}
}

document.getElementById("job_form").addEventListener("submit", (event) => {
  event.preventDefault();
  update_job_handler();
});




		

async function delete_job_handler()
	{
	var jn = get_job_number();
	if (confirm('Delete job "'+jn+'" and any cores with this job_number?')) 
	{
		fetch(host+'/delete_job/'+jn,{method: 'delete'})
		.then(response => response.json())
		.then(data => {
			console.log(data);
			console.log('deleted job');
			update_jobs();
			}
			)
	.catch(error => console.error(error));
	}}


async function update_job_form(job_number){
//	console.log('update_job_form:'+job_number);
	fetch("/get_job_details?job_number="+job_number)
	.then(response => response.json())
	.then(data => 
		{console.log(data);
		setForm(document.getElementById("job_form"),data);
		})
	.catch(error => console.error(error));
	}
		


function set_options(sel,values,default_opt){
	arrOptions = [];
	values.forEach((v) => arrOptions.push("<option>" + v + "</option>"))
	sel.innerHTML = arrOptions.join();
	i = values.indexOf(default_opt);
	sel.value = default_opt;
	//console.log('selected ind:'+i);
	return i;
}


function job_changed(){
	jn = get_job_number();
	window.location.href = "/static/jobs.html?job_number="+jn;
}


async function update_jobs()
{
	const urlParams = new URLSearchParams(window.location.search);
	const current = urlParams.get('job_number');
	toLoad = ' ';
	i = 0;
	
	var s = document.getElementById("job_select");
	fetch("/get_job_numbers")
	.then(response => response.json())
	.then(data => 
		{
	//	console.log(data);
		i = set_options(s,data,current);
		if (i != -1){update_job_form(data[i]);}
		else {update_job_form(' ');}
		})
		
	.catch(error => {
		console.error(error);		
		update_job_form(' ')});
}


