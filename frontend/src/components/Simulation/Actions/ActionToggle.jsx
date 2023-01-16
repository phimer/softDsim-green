import { Grid, Button } from "@chakra-ui/react"
import React, { useState } from "react";

const ActionToggle = (props) => {

    const [buttonValue, setButtonValue] = useState(false)

    function handleButtonClick() {
        setButtonValue(!buttonValue)
        props.onEventbutton(!buttonValue)
    }

    return (
        <>
            <Grid justifyItems='center'>
                <Button
                    colorScheme={buttonValue ? 'blue' : 'blackAlpha'} size='lg'
                    onClick={handleButtonClick}
                >
                    {buttonValue ? props.textTrue : props.textFalse}
                </Button>
            </Grid>
        </>
    )
}

export default ActionToggle