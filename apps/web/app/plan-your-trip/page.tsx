import type { Metadata } from 'next';
import { Container, PageHero } from '../../components/ui';

export const metadata: Metadata = { title: 'Plan Your Costa Rica Trip', description: 'Share your travel style and interests to start planning a personalized Costa Rica experience.' };

const groups = ['Couple', 'Family', 'Friends', 'Solo', 'Group'];
const styles = ['Adventure', 'Relaxation', 'Nature', 'Wildlife', 'Romance', 'Culture', 'Mixed'];
const activityLevels = ['Relaxed', 'Moderate', 'Active'];
const interests = ['Volcanoes', 'Rafting', 'Hot springs', 'Wildlife', 'Hiking', 'Waterfalls', 'Coffee', 'Chocolate', 'Photography'];

function ChoiceGroup({ legend, name, options, multiple = false }: { legend: string; name: string; options: string[]; multiple?: boolean }) {
  return <fieldset className="choice-group"><legend>{legend}</legend><div className="choice-grid">{options.map((option) => { const id = `${name}-${option.toLowerCase().replace(/ /g, '-')}`; return <label className="choice" htmlFor={id} key={option}><input id={id} name={name} type={multiple ? 'checkbox' : 'radio'} value={option} /><span>{option}</span></label>; })}</div></fieldset>;
}

export default function PlanYourTripPage() {
  return (
    <main id="main-content">
      <PageHero eyebrow="Start with your travel style" title="What would make this trip feel like yours?" intro="Tell us what you’re drawn to. This early planning worksheet will help shape the future personalized trip-planning experience." />
      <section className="section planner-section"><Container className="planner-layout">
        <aside className="planner-aside"><p className="eyebrow">A simple beginning</p><h2>There is no wrong way to experience Costa Rica.</h2><p>Choose whatever sounds most like you. Your answers are not submitted or saved yet.</p><ol><li><span>1</span>Your group</li><li><span>2</span>Your travel style</li><li><span>3</span>Your interests</li><li><span>4</span>Contact details</li></ol></aside>
        <form className="planning-form">
          <div className="form-section"><span className="form-section__number">01</span><ChoiceGroup legend="Who is traveling?" name="travel-party" options={groups} /></div>
          <div className="form-section"><span className="form-section__number">02</span><ChoiceGroup legend="What kind of trip are you imagining?" name="trip-style" options={styles} multiple /></div>
          <div className="form-section"><span className="form-section__number">03</span><ChoiceGroup legend="What activity level feels right?" name="activity-level" options={activityLevels} /></div>
          <div className="form-section"><span className="form-section__number">04</span><ChoiceGroup legend="What are you interested in?" name="interests" options={interests} multiple /></div>
          <div className="form-section"><span className="form-section__number">05</span><fieldset className="contact-fields"><legend>How can we reach you?</legend><div className="field-grid"><label>Full name<input name="name" type="text" autoComplete="name" placeholder="Your name" /></label><label>Email address<input name="email" type="email" autoComplete="email" placeholder="you@example.com" /></label></div><label>Phone <small>(optional)</small><input name="phone" type="tel" autoComplete="tel" placeholder="Include country code" /></label></fieldset></div>
          <div className="form-status" role="note"><p><strong>Planning preview</strong> This form is not connected yet, so your answers will not be sent or saved.</p><button type="button" disabled>Submit planning request</button></div>
        </form>
      </Container></section>
    </main>
  );
}
