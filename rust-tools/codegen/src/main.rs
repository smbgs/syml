use serde_json::{json};

use syml_core::{Service};

fn main() -> std::io::Result<()> {
    let mut service = Service::new("rust-codegen");

    service.cmd("generate_struct_from_scheme", |cmd| {
            print!("{:?}", cmd);

            // TODO: actually implement the rust codegen using  something like
            //  https://github.com/carllerche/codegen
            return json!({
                "some_data": "some_value"
            });
        }
    );

    service.serve()?;

    Ok(())
}
