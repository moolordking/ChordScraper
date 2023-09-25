
let IN  = document.getElementById("IN");
let OUT = document.getElementById("OUT");

function update_out() {
	let raw = IN.value;
	let processed = "";
	let seperated = raw.split("\n");
	for (let line=0; line<seperated.length; line++) {
		processed += "<p class='LINE'>";
		processed += seperated[line]
			// .replace(/>>.<</, ", ")
			.replaceAll("<<", "<span class='CHORD'>")
			.replaceAll(">>", "</span>")
			.replaceAll("[","<span class='TITLE'>")
			.replaceAll("]","</span>");
		processed += "</p>";
	}
	OUT.innerHTML = processed + "<br>";
}

function show_hide() {
	if (IN.style.display != "none") {
		IN.style.display = "none";
	} else {
		IN.style.display = "initial";
	}
}

function download_image() {
    let container = OUT;
    IN.style.display = "none";
    html2canvas(container, { allowTaint: true }).then(function (canvas) {
        var link = document.createElement("a");
        document.body.appendChild(link);
        link.download = prompt("Name: ") + ".jpg";
        link.href = canvas.toDataURL();
        link.target = '_blank';
        link.click();
    });
}

update_out();
