        function getEventsByLocation(div){

          var eventsFiltered = []
          locationString = div.target.id;
          if(eventList != false){
            eventsFiltered=eventList.filter(function(event){
              return event.location==locationString;
            })
            if(eventsFiltered.length>0){
              $(".loc-box").fadeOut("fast");
  
              btn = document.getElementById("back-button");
              btn.classList.toggle("invisible");
              elements = document.getElementsByClassName("loc-box");
              generateEventsPage(eventsFiltered);
            }
            else{alert("Ne pare rau. In acest moment nu se poate face programare pentru locatia selectata.")}
          }
          else{alert("Ne pare rau. In acest moment nu se poate face programare pentru locatia selectata.")}
          }
          
          
        function generateEventsPage(eventsFiltered){
          $(".loc-box").fadeOut();

          var mainDiv = document.getElementById("location-event");
          for(var ev in eventsFiltered){
            var article = eventsFiltered[ev];
            var newDiv = document.createElement('div');
            newDiv.id = ev;
            if(article.is_lawyer=='false'){
              newDiv.classList=["location-elem col-sm-3 border border-secondary rounded shadow ev-box"];
            }
            else{
              lawyerParagraph = document.createElement('p');
              lawyerParagraph.className="lawyerparagraph";
              lawyerParagraph.innerHTML="FORMULAR DESTINAT EXCLUSIV AVOCATILOR";
              newDiv.appendChild(lawyerParagraph);
              newDiv.classList=["location-elem-lawyer col-sm-3 border 1 border-danger rounded shadow ev-box"];
            }
            newDescription=document.createElement('div');
            newDescription.className="location-details";
            newDescription.innerHTML=article.details;
            var newTitle = document.createElement('div');
            newTitle.innerHTML=article.name;
            newTitle.className="location-title border-bottom border-info";
            button = document.createElement('button');
            button.className="btn btn-info location-button"
            button.innerHTML="SELECTEAZA"
            button.id=article.name;
            button.addEventListener("click", function(){alert('test')} , false);
            newDiv.appendChild(newTitle);
            newDiv.appendChild(newDescription);
            newDiv.appendChild(button);
            mainDiv.appendChild(newDiv);
          }
        }

        function backbutton(){
          $(".ev-box").fadeOut("fast");
          $(".loc-box").fadeIn();
          btn = document.getElementById("back-button");
            btn.classList.toggle("invisible");
            
        }

        document.addEventListener('DOMContentLoaded', (event) => {
          generateLocationsPage();
        
          })

          function generateLocationsPage(){
            var mainDiv = document.getElementById("location-event");
            for(var loc in locList){
              var location = locList[loc]; 
              var newDiv = document.createElement('div');
              newDiv.id = loc;
              newDiv.classList=["location-elem col-sm-3 border border-secondary rounded shadow loc-box"];
              newDescription=document.createElement('div');
              newDescription.className="location-details";
              newDescription.innerHTML=location.details;
              var newTitle = document.createElement('div');
              newTitle.innerHTML=location.name;
              newTitle.className="location-title border-bottom border-info";
              button = document.createElement('button');
              button.className="btn btn-info location-button"
              button.innerHTML="SELECTEAZA"
              button.id=location.name;
              button.addEventListener("click", getEventsByLocation , false);
              newDiv.appendChild(newTitle);
              newDiv.appendChild(newDescription);
              newDiv.appendChild(button);
              mainDiv.appendChild(newDiv);
              
            }
          }