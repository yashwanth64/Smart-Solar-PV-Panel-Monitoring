(define (domain SMSDomainFile)

    (:requirements
        [:adl]
    )

    (:types
        
        actuator sensor - object
        actSensor - sensor
        temperature dust - actSensor
		dustActuator temperatureActuator - actuator


    )


    (:predicates
    
        ;; for sensor
        (isHigh ?x - actSensor)
        ;;for actuator
        (isOn ?x - actuator)

    )


;;action section 
    ;;for actuators
    (:action turnOFF 
        :parameters (?s - actSensor ?a - actuator)
        :precondition (and (not(isHigh ?s)) (not(isOn ?a)))
        :effect (isOn ?a)
    )
    
    (:action turnON 
        :parameters (?s - actSensor ?a - actuator)
        :precondition (and (isHigh ?s) (isOn ?a))
        :effect (not(isOn ?a))
    )
    
    
)   