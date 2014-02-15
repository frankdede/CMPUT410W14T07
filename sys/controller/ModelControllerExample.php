<?php
$root = $_SERVER['DOCUMENT_ROOT'];
require_once $root . '/../sys/controller/PDO_Helper.php';
require_once $root . '/../sys/model/Vet.php';		
require_once $root . '/../sys/model/Pet.php';	
require_once $root . '/../sys/model/Clinic.php';	
require_once $root . '/../sys/model/Interest.php';	
require_once $root . '/../sys/model/Picture.php';	
require_once $root . '/../sys/model/PatientOwner.php';
require_once $root . '/../sys/model/AchievementRecord.php';

class ModelController {	

	private $helper;


	public function __construct() {
		$this->helper = new PDOHelper();
	}

	/**
 	* Returns vet object if email is valid otherwise return null
 	* @param  String $p_email
 	* @return Vet Model Object
 	*/
	public function getVetObject($p_email){
		$vet = new vet();
		$vet->findEmail($p_email);

		//Find the provided email in db, return with password and salt if valid, else returns null
		$result = $this->helper->checkEmailQuery("vet",$p_email);
		if(is_null($result['email'])){
			return null;
		}else {
			$vet->setEmail($result['email']);
			$vet->setPass($result['pass']);
			$vet->setSalt($result['salt']);
			return $vet;
		}
/*
		//Check if email, password, and salt fields are set. If not return NULL
		if (is_null($vet->getEmail()) || is_null($vet->getPassword()) 
		  || is_null($vet->getSalt())){
			return null;
		} else {
			return $vet;
		}
*/
	}

	/** NOT IMPLEMENTED PROPERLY getVetObject already returns the object itself with all info
	 * Parameter has to be vet object, returns the same vet object with populated fields
	 * @param  Vet Model Object $vet
	 * @return Vet Model Object
	 */
	public function getVetInfo($vet){
		$vet->setInfo();
		return $vet;
	}

	/** NOT IMPLEMENTED CORRECTLY
	 * Get patient owner information
	 * @param  [string] $p_clinic_id  [Clinic ID]
	 * @param  [string] $p_patient_id [Patient ID]
	 * @return [object]               [Patient Owner object with populated fields]
	 */
	public function getPatientOwnerObject($p_clinic_id, $p_patient_id){
		$result =  $this->helper->getOwnerInfo($p_clinic_id, $p_patient_id);
		if($result['count']==1){
			$owner = new PatientOwner();
			$owner->setInfo($result);
			return $owner;
		}else{
			return null;
		}
	}

	/**
	 * Get achievement record information
	 * @param  [string] $p_achievement_id  [Achievement ID]
	 * @param  [string] $p_pet_id 		   [Pet ID]
	 * @return [object]               	   [Achievement Record Object with fields]
	 */
	public function getAchievementRecordObject($p_achievement_id, $p_pet_id){
		$result =  $this->helper->getAchievementRecordInfo($p_achievement_id, $p_pet_id);
		var_dump($result);
		if(count($result)>=1){
			$achievementRecord = new AchievementRecord();
			$achievementRecord->setInfo($result[0]);
			return $achievementRecord;
		}else{
			return null;
		}
	}

	/**
	 * [Gets all clinic object info]
	 * @return [Array] $array [An array of clinic objects]
	 */
	public function getClinics(){
		$result = $this->helper->getAllClinicInfo();
		$array = array();
		for($i=0;$i< sizeof($result); $i++){
			$clinic = new Clinic();
			$clinic->setInfo($result[$i]);
			array_push($array,$clinic);
		}
		return $array;
	}

	/**
	 * [Gets all interest object info based on pet ID]
	 * @return [Array] $array [An array of interest objects]
	 */
	public function getInterests($p_pet_id){
		$result = $this->helper->getAllInterestInfo($p_pet_id);
		$array = array();
		for($i=0;$i<sizeof($result);$i++){
			$interest = new Interest();
			$interest->setInfo($result[$i]);
			array_push($array,$interest);
		}
		return $array;
	}

	/**
	 * [Gets all picture object info based on pet ID]
	 * @return [Array] $array [An array of picture objects]
	 */
	public function getPictures($p_pet_id){
		$result = $this->helper->getAllPictureInfo($p_pet_id);
		$array = array();
		for($i=0;$i<sizeof($result);$i++){
			$picture = new Picture();
			$picture->setInfo($result[$i]);
			array_push($array,$picture);
		}
		return $array;
	}

	/**
	 * [Gets the pet model object]
	 * @param  [String] $p_pet_id [The pet registration ID]
	 * @return [Pet] $pet [Pet Model Object]
	 */
	public function getPet($p_pet_id){
 		//Getting the array of interest objects for this pet
        $result = $this->helper->getPetInfoQuery($p_pet_id);
        if(count($result)==0) {
            return null;
        } else {
 			//Getting the array of interest objects for this pet
            $interestArray = $this->getInterests($p_pet_id);
            
 			//Getting the array of picture objects for this pet
            $pictureArray = $this->getPictures($p_pet_id);
            //Creating the empty array for putting picture objects

            $pet = new Pet(); 
		    $pet->setInfo($result[0],$pictureArray,$interestArray);
            return $pet;
        }
	}

	/** 
	 * Update the photo likes by 1
	 * @param  [ID] $p_pet_id [Pet ID]
 	 * @param  [ID] $p_pic_id [Pic ID]
	 * @return [Bool]  [True or False depending on success]
	 */
	public function updatePictureLikes($p_pet_id, $p_pic_id){
		return $this->helper->updatePictureLikes($p_pet_id, $p_pic_id);
	}
	
	/** 
	 * Update the photo views by 1
	 * @param  [ID] $p_pet_id [Pet ID]
 	 * @param  [ID] $p_pic_id [Pic ID]
	 * @return [Bool]  [True or False depending on success]
	 */
	public function updatePictureViews($p_pet_id, $p_pic_id){
		return $this->helper->updatePictureViews($p_pet_id, $p_pic_id);
	}
	
	/**
	 * Translates key values in associative array providing values for
	 * pet model from "client side" camelCase style to the keys
	 * used by the db.
	 * @param: associate array providing values for patient model with
	 * 		   key values in the format expected/provided by the client
	 *		   side
	 * @return: an associate array as described above.
	 */
	function petToDbArray($petDef) {
		return array(
			'pet_id' 	    => 	$petDef['petId'],
			'birthday' 	    =>	$petDef['petBirthday'],
			'pet_name'      =>	$petDef['petName'],
			'sex' 		    =>	$petDef['petSex'],
			'age' 		    =>	$petDef['petAge'],
			'colour'	    => 	$petDef['petColour'],
			'breed' 	    =>	$petDef['petBreed'],
			'species' 	    =>	$petDef['petSpecies'],
            'isNeutered'    =>	$petDef['petNs'],
            'netPoints'     =>  $petDef['petNetPoints']
		);
	}


	/**
	 * Translates key values in associative array providing values for
	 * patient owner model from "client side" camelCase style to the keys
	 * used by the db.
	 * @param: associate array providing values for patient owner model with
	 * 		   key values in the format expected/provided by the client
	 *		   side
	 * @return: an associate array as described above.
	 */
	function ownerToDbArray($ownerDef) {
		$dbArray = array(
			'patient_id' 	=>	$ownerDef['patientId'],
			'clinic_id' 	=> 	$ownerDef['clinicId'],
			'firstname' 	=>	$ownerDef['ownerFirstName'],
			'lastname' 		=>	$ownerDef['ownerLastName'],
			'address' 		=>	$ownerDef['ownerAddress'],
			'city' 			=>	$ownerDef['ownerCity'],
			'province' 		=>	$ownerDef['ownerProvince'],
			'postal_code' 	=>	$ownerDef['ownerPostalCode'],
			'home_number'	=>	$ownerDef['ownerHomeNumber'],
			'cell_number' 	=>	$ownerDef['ownerCellNumber'],
			'email' 		=>	$ownerDef['ownerEmail'],
			'hasOptedIn'	=>	$ownerDef['ownerPs']
		);

		// Add owner id separately as it is not always the case that it will be
		// passed from the front-end (that is, in cases of edits and deletes it
		// will be, but in the case of creation it will not be)
		if (isset($ownerDef['ownerId'])) {
			$dbArray['owner_id'] = $ownerDef['ownerId'];
		}

		return $dbArray;
    }


    /**
     * Add a picture 
     * @param: [String] $p_pet_id [The pet ID]
     * @param: [String] $p_path    [The picture path]
     * @param: [String] $p_description  [The description of the picture]
     * @return: [String] [The unique Picture ID]
     */
    public function addPicture($p_pet_id, $p_path, $p_description){
        return $this->helper->addPicture($p_pet_id,$p_path,$p_description);
    }

    /**
     * Update a picture's description 
     * @param: Array $p_picture
     * @return: boolean true if the operation is successful, otherwise false
	 */
    public function updatePictureDescription($p_picture){
        return $this->helper->updatePictureDescription($p_picture);
    }
        
    /**
     * Delete a picture
     * @param: String $p_petId $p_picId
     * @return: boolean true if the operation is successful, otherwise false
	 */
    public function deletePicture($p_petId,$p_picId){
        return $this->helper->deletePicture($p_petId,$p_picId);
    }
}	
?>
