var name = "Sebastiani Aguirre-Navarro";
var formattedName = HTMLheaderName.replace("%data%", name);


var role = "Software Developer";
var formattedRole = HTMLheaderRole.replace("%data%", role);
$("#header").prepend(formattedRole);
$("#header").prepend(formattedName);


var bio = {
    "name": "Sebastiani Aguirre-Navarro",
    "role": role,
    "contact": {
	"mobile": "787-469-4138",
	"email": "sebastiani.aguirre@upr.edu",
	"github": "sebastiani",
	"twitter": "@evapilot",
	"location": "Puerto Rico"
    },
    "welcomeMessage": "lorem ipsum dolor sit amet",
    "skills": ["Java", "Python", "C++", "Algorithms", "EVA Piloting"], 
    "picture": null
};

var work = {
    "jobs" : [
	{
	    "position":"Co-op Student",
	    "employer": "DoD",
	    "years": "1",
	    "description": "Being awesome"
	},
     ]
};

var education = {
    "schools":[
	{ "name": "University of Puerto Rico",
	  "years": "2010-2016",
	  "city": "Mayaguez, Puerto Rico"
	}
    ],
    "onlineCourses": [
	{ 
	    "name": "JavaScript Syntax",
	    "school": "Udacity",
	    "dates": "2015",
	    "url": "http://www.udacity.com/course/ud804"
	}
    ]

};

if(bio.skills.length > 0){
    $("#header").append(HTMLskillsStart);
    for(i in bio.skills){
	skill = HTMLskills.replace("%data%", bio.skills[i]);
	$("#skills").append(skill);
    }
}

if(work.jobs.length > 0){
    $("#workExperience").append(HTMLworkStart);
    for( i in work.jobs){
	job = work.jobs[i];
	displayWork()
    }
}

function displayWork(){
	employer = HTMLworkEmployer.replace("%data%", job.employer);
	title = HTMLworkTitle.replace("%data%", job.position);
	$(".work-entry:last").append(employer+title);
}

education.display = function() {
    //code goes here
}

$("#mapDiv").append(googleMap);
