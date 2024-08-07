import './App.css';

function job_change() {
	alert("job changed");
}


function JobSelect() {
	
	let jobs = [{row:1,number:"job1"},{row:2,number:"job2"},{row:3,number:"job3"}]

	
	return (
		<select name = "jobs" onchange = "job_change()" id="job-select">
		  <option value="">--Please choose an option--</option>		  
		  {jobs.map((j) => (<option value = {j.row} > {j.number} </option>))}
		</select>
	);
}




function App() {
	

	
  return (
    <div className="App">
	  	
		<p>
			<JobSelect/>
			<button>previous</button>
			<button>next</button>
		</p>
	
    </div>
  );
}

export default App;



