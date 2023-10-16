

export function formatToLocalTime(utcTime) {
    // Create a Date object from the UTC time
    const utcDate = new Date(utcTime);

    // Format the date and time to the user's locale and timezone
    const formattedTime = utcDate.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    timeZoneName: 'short',
    hour12: false,
    });

    return formattedTime;
}

// Function to calculate the difference between two datetime values
export function calculateDatetimeDifference(datetime1) {
    // Parse the datetime strings into Date objects
    const date1 = new Date(datetime1);
    const date2 = new Date();

    // Calculate the time difference in milliseconds
    const timeDifference = Math.abs(date1 - date2);

    // Calculate the difference in days, hours, minutes, and seconds
    const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);
    
    if (seconds > 0){
        if(minutes > 0){
            if(hours > 0){
                if(days > 0){
                    return days.toString()+" days "+hours.toString()+" hours "+minutes.toString()+" minutes "+seconds.toString()+" seconds ago"
                }
                return hours.toString()+" hours "+minutes.toString()+" minutes "+seconds.toString()+" seconds ago"
            }
            return minutes.toString()+" minutes "+seconds.toString()+" seconds ago"
        }
        return seconds.toString()+" seconds ago"
    }
}