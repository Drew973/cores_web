// @generated automatically by Diesel CLI.

diesel::table! {
    job (job_number) {
        job_number -> Text,
        client -> Nullable<Text>,
        project -> Nullable<Text>,
    }
}
