#[macro_use] extern crate rocket;
use rocket::fs::{FileServer, relative};
use rocket::form::Form;
use rocket::serde::Serialize;
use rocket::serde::json::Json;
//use postgres::{Client, NoTls,Transaction};
//use rocket_db_pools::{sqlx, Database};
use rocket::diesel::PgPool;


//#[derive(Database)]
//#[database("sqlite_logs")]
//struct Logs(sqlx::SqlitePool);


#[derive(Serialize)]
#[serde(crate = "rocket::serde")]
#[derive(FromForm)]
struct Job {
	//#[field(validate=len(1..))]
    job_number: String,
    client: String,
    project: String,
}

//html forms don't support put?! using upsert instead.
#[post("/upsert_job", data = "<j>")]
fn upsert_job(j : Form<Job>) -> String
{
	let result:String = format!("Sucessfully edited job. job_number : {},client:{},project:{}", j.job_number,j.client,j.project);
	return result
}


#[get("/")]
fn index() -> &'static str {
    "Hello, world!"
}


//route.
#[get("/hello/<name>")]
//this function is a handler 
fn hello(name: &str) -> String {
    format!("Hello, {}!", name)
}
//http://127.0.0.1:8000/hello/me -> Hello, me


#[get("/get_job/<job_number>")]
fn get_job(job_number:&str) -> Json<Job>
{
	Json(Job {job_number:String::from(""),client:String::from(""),project:String::from("")})
}

//http://127.0.0.1:8000/index.html

#[launch]
fn rocket() -> _ {
	rocket::build().mount("/", routes![index])
		.mount("/", routes![hello])//http://127.0.0.1:8000/hello 
		.mount("/", routes![upsert_job])//http://127.0.0.1:8000/upsert_job
		.mount("/", routes![get_job])//http://127.0.0.1:8000/get_job
		.mount("/", FileServer::from(relative!("../frontend/javascript_only")))
	//	.attach(Logs::init())
}


//http://127.0.0.1:8000/static goes to index.html
//http://127.0.0.1:8000/static/page1.html goes to page1.html