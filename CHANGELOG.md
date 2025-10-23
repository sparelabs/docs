## 2025-10-17 - Daily Update

# Release Summary - Friday, October 17, 2025

*What's New in Spare*

---
## 🤖 AI Voice

### 🗣️ More Accurate Date of Birth Recognition

**What's New**  
AI Voice is now more precise when handling dates of birth for rider authentication. It is stricter about ambiguous formats and better at understanding various spoken date formats to improve the success rate of voice authentication.

**Pre-requisites**
- Requires AI Voice to be enabled for the organization.

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- This is a non-visual improvement to the background processing of the AI Voice call flow during rider authentication.

**What You Can Do**
- Riders can authenticate using dates like "June 6th 2025" or "2025 06 01," and the system will correctly understand them.
- The system will now reject ambiguous dates like "one one ninety two" (which could be January 1st or November 1st) to prevent incorrect authentications.

**Why This Matters**  
Inaccurate date recognition could lead to failed authentications or, in rare cases, authenticating the wrong rider. This improvement increases the reliability and security of the AI Voice authentication process by correctly handling clear date formats and rejecting ambiguous ones.

</details>

---
## 🎯 Operations

### ⏱️ Smarter Duty Interruption Scheduling

**What's New**  
When creating a duty interruption, the system now intelligently handles situations where the duty is ending soon. If the full interruption doesn't fit, the system will automatically schedule a shorter one if possible and notify you of the change.

**Pre-requisites**
- Requires Administrator access with permissions to manage duties.

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- *Rides > Live Map > (Select a Duty) > Breaks tab > Add Break button*

**What You Can Do**
- When you create an interruption near the end of a duty:
  - If the full duration fits, it will be created as requested.
  - If only a partial duration fits, the interruption will be created for that shorter duration, and a notification will inform you (e.g., "Interruption created but shortened to 15 minutes").
  - If it doesn't fit at all, you'll receive a clear failure message (e.g., "Could not create interruption as there is not enough time remaining in the duty").

**Why This Matters**  
Previously, attempting to create an interruption that didn't fit within the remaining duty time would simply fail without a clear explanation. This enhancement provides better feedback and automatically adjusts the break when possible, creating a more intuitive workflow for dispatchers.

</details>

---
### 🐛 Bug Fixes

- **Service Availability During Fare Estimation (BUS-3786)**
  - _Resolution_: Fixed an issue where some services were not appearing as available during fare estimation due to time-based rules on their service zones. The system now validates geography first to show available services, and applies time validation only after a specific trip time is selected.

---
## 📊 Analytics

### 📊 Query Group Membership Custom Fields

**What's New**  
Custom fields associated with Group Memberships are now directly available for querying in Analytics V2. This allows for building more detailed reports based on custom data stored on group memberships.

**Pre-requisites**
- Requires `AnalyticsV2` feature flag.

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- *Analytics > Query Builder* (when using the `Group Memberships` data source).

**What You Can Do**
- In the Query Builder, select the `Group Memberships` data source.
- You will now see your custom fields (e.g., `metadata_field_name`) available as dimensions for filtering, grouping, and display.

**Why This Matters**  
Previously, accessing group membership custom fields was difficult and limited. This change makes that data a first-class citizen in Analytics, enabling richer reports on rider segments, eligibility, and other custom-tracked attributes.

</details>

---
### 🔗 Link Case Assignees to Admin Details in Reports

**What's New**  
In Analytics V2, you can now join `Case Data` with `Organization Admin` data. This allows you to include details about the assigned administrator (like their name or phone number) in reports about cases.

**Pre-requisites**
- Requires `AnalyticsV2` feature flag.

<details>
<summary><strong>See More</strong></summary>

**Where You'll See It**
- *Analytics > Query Builder*

---

## 2025-10-22 - Daily Update

# Release Summary - Wednesday, October 22, 2025

*What's New in Spare*

---

## ✨ New Features

### Work Order Categories

**What's New**
You can now create and manage custom categories for your work orders within the Enterprise Asset Management (EAM) section. This helps you organize and classify work more effectively.

**Where You'll See It**
You'll find a new "Work Order Categories" section under the "Settings" in the main sidebar. When creating or editing work orders, you'll see a new field to select a category.
- **Requires `EamMfe`**

**What You Can Do**
You can define specific categories like "Vehicle Maintenance," "Facility Repair," or "Safety Check." Then, you can assign these categories to individual work orders, making it easier to filter, sort, and analyze your maintenance tasks.

**Why This Matters**
This feature brings more structure to your work order management, allowing for better reporting and quicker identification of related tasks. It simplifies tracking and ensures your team can easily find and manage work orders based on their type.

---

## 🚀 Feature Enhancements

### Improved Service Discovery for East Bay Paratransit (EBP)

**What's New**
When you're browsing for East Bay Paratransit (EBP) services, the system will now show you all available options, even if the current time falls outside of their regular operating hours. This means you can see the full range of services without being restricted by time.

**Where You'll See It**
This improvement affects how EBP services appear in the service selection dropdown when you are performing a service discovery or estimating a trip.

**What Changed**
- **Before**: If you were looking for an EBP service outside its operating hours (e.g., late at night), it might not have appeared in your search results, even if you were just trying to see what services were available.
- **Now**: All EBP services will be visible during service discovery, regardless of the time you're searching. Time validation will still apply when you actually try to book a trip, ensuring you only book within operating hours.

**Why This Matters**
This enhancement gives you a complete picture of available EBP services at any time, making it easier to plan future trips or understand the full scope of service offerings without being artificially limited by time constraints during your initial search.

### Enhanced Rider Location on Driver App Map

**What's New**
The driver app now displays rider locations with more dynamic and visually engaging markers on the map. These new markers are circular, customizable, and can animate smoothly as the rider moves.

**Where You'll See It**
Drivers will see these enhanced markers on their map within the driver application when a rider is sharing their location.

**What Changed**
- **Before**: Rider location markers were static and less customizable.
- **Now**: Rider locations are shown with modern, customizable circular badges that can include labels, colors, and borders. These markers also animate smoothly when the rider's position updates, providing a more intuitive real-time view.

**Why This Matters**
This update provides drivers with a clearer and more engaging visual representation of rider locations, especially when riders are on the move. The smooth animations help drivers quickly and accurately track their passengers, reducing confusion and improving pickup efficiency.

---

## 🐛 Bug Fixes

-   **Cannot Clear Province/State in Address (ENG-835)** - Previously, when editing an address in a rider's profile, you couldn't clear the "Province/State" or "Country" fields because the "None" option was disabled. Now, you can easily select "None" from the dropdowns to clear these fields, allowing you to completely remove an address if needed.

---

_Generated from 6 merged PRs | 4 customer-impacting changes_

---

