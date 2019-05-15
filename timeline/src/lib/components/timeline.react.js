import React, {Component} from 'react';
import PropTypes from 'prop-types';
import { Timeline, TimelineItem }  from 'vertical-timeline-component-for-react';
import './timeline.css'

/**
 * ExampleComponent is an example component.
 * It takes a property, `label`, and
 * displays it.
 * It renders an input with the property `value`
 * which is editable by the user.
 */
export default class timeline extends Component {
    render() {
        return( 
        <Timeline className="timeLineContent" lineColor={'#061D20'}>
        <TimelineItem
          key="001"
          dateText="March 31, 2015"
          style={{ color: '#FEF7EC' }}
        >
          <h3> Phillip White </h3>
          <h4> Vineland, New Jersey </h4>
          <p>
            "Phillip White died in police custody. The polices were responding to a call reporting White's erractic behaviors. After the polices arrived, they called
            for medical assistant and White were handcuffed and put it a vehical to the hospital. He was reportedly died in the hospital"
          </p>
          <p>
            "There were cellphones recording the arresting scenes at the time. It appeared to be that White was biten by police dogs. The officers involved
            in the case was not charged."
          </p>
          <p> <a href="https://www.nbcphiladelphia.com/news/local/Vineland-Police-Chief-PCP-Phillip-White-Death-K-9-Dog-Codispoti-Timothy-Anonymous-Hacking-GroupThreats-299103451.html">Source</a></p>
        </TimelineItem>
        <TimelineItem
          key="002"
          dateText="April 4, 2015"
          dateInnerStyle={{ color: '#FEF7EC' }}
        >
          <h3>Walter Scott</h3>
          <h4>North Charleston, South Carolina</h4>
          <p>
          "The Shooting of Walter Scott occurred on April 4, 2015, in North Charleston, South Carolina, following a daytime traffic stop for a non-functioning brake light. 
          Scott, an unarmed black man, was murdered by Michael Slager, a white North Charleston police officer.
          Slager was charged with murder after a video surfaced which showed him shooting Scott from behind while Scott was fleeing, and which contradicted his police report."
          </p>
          <p>
          <a href="https://en.wikipedia.org/wiki/Shooting_of_Walter_Scott">Source</a>
          </p>
        </TimelineItem>
        <TimelineItem
          key="003"
          dateText="April 19, 2015"
          style={{ color: '#FEF7EC' }}
        >
          <h3> Freddie Gray  </h3>
          <h4> Baltimore </h4>
          <p>
          "On April 12, 2015, Freddie Carlos Gray, Jr., a 25-year-old black man, was arrested by the Baltimore Police Department for
           possessing what the police alleged was an illegal knife under Baltimore law.
           While being transported in a police van, Gray fell into a coma and was taken to a trauma center.
            Gray died on April 19, 2015; his death was ascribed to injuries to his spinal cord."
          </p>
          <p> <a href="https://en.wikipedia.org/wiki/Death_of_Freddie_Gray">Source</a></p>
        </TimelineItem>
        <TimelineItem
          key="004"
          dateText="September 20, 2016"
          style={{ color: '#FEF7EC' }}
        >
          <h3> Keith Lamont Scott  </h3>
          <h4> Charlotte, North Carolina  </h4>
          <p>
          "Keith Lamont Scott, a 43-year-old African-American man, was fatally shot on September 20, 2016, in Charlotte, North Carolina.
          Police officers had arrived at Scott's apartment complex to search for an unrelated man with an outstanding warrant. 
          According to police, officers saw Scott exit a vehicle in the parking lot while carrying a handgun, and he refused to comply with their orders. 
          Scott's wife was also present and disputed that account."
          </p>
          <p> <a href="https://en.wikipedia.org/wiki/Shooting_of_Keith_Lamont_Scott">Source</a></p>
        </TimelineItem>
      </Timeline>
        )
    }
}

timeline.defaultProps = {};

timeline.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks
     */
    id: PropTypes.string,

    /**
     * A label that will be printed when this component is rendered.
     */
    label: PropTypes.string.isRequired,

    /**
     * The value displayed in the input
     */
    value: PropTypes.string,

    /**
     * Dash-assigned callback that should be called whenever any of the
     * properties change
     */
    setProps: PropTypes.func
};
