import { utcToZonedTime, format } from 'date-fns-tz'

function StringToPrettyDate(string) {
  if (string !== undefined) {
    const date = new Date(string)
    const zonedDate = utcToZonedTime(date, 'Europe/Berlin')
    const pattern = "dd.MM.yyyy HH:mm z '(Europe/Berlin)'"
    // return format(zonedDate, pattern, { timeZone: 'Europe/Berlin' })
    return format(date, "dd.MM.yyyy, HH:mm (z)")
  } else {
    return "-"
  }
}

// function StringToPrettyDate(string) {
//   const serverDateString = string + '+01:00'
//   const date = new Date(serverDateString);

//   // Detect user's preferred locale
//   // const userLocale = navigator.language || 'en-US'; // Fallback to 'en-US' if the browser doesn't provide a language
//   // const userLocale = Intl.DateTimeFormat().resolvedOptions().locale || 'sv-SE'; // Fallback to 'sv-SE' = ISO 8601 if the browser doesn't provide a language
//   const userLocale = 'sv-SE'; // ISO 8601 format

//   // Detect user's time zone
//   const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;


//   // Set the options for formatting the date
//   const options = {
//     day: '2-digit',
//     month: '2-digit',
//     year: 'numeric',
//     hour: '2-digit',
//     minute: '2-digit',
//     timeZoneName: 'short',
//     timeZone: userTimeZone,
//   };

//   // Format the date using toLocaleString
//   const formattedDate = date.toLocaleString(userLocale, options);
//   const outputString = `${formattedDate} (${userTimeZone})`;

//   return outputString;
// }

export default StringToPrettyDate
