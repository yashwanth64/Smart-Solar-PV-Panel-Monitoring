(define (problem SMSProblem)

    (:domain SMSDomainFile)
    
    (:objects 
		 SRT0100 - temperature
		 SDS0100 - dust
		 ARA0100 - temperatureActuator
		 ADA0100 - dustActuator

    )
    
    (:init   
		(isOn ARA0100)
		(isHigh SDS0100)
		(isOn ADA0100)

    )
         
    (:goal 
        ( and

			(or
				(and (isHigh SRT0100) (not(isOn ARA0100)) )
				(and (not(isHigh SRT0100)) (isOn ARA0100) ) 
			) ;or SRT0100 ARA0100

			(or
				(and (isHigh SDS0100) (not(isOn ADA0100)) )
				(and (not(isHigh SDS0100)) (isOn ADA0100) ) 
			) ;or SDS0100 ADA0100


                  
        )
    ) 

)