<?php
$root = $_SERVER['DOCUMENT_ROOT'];
require_once $root . '/../sys/controller/PDO_Adapter.php';
class PDOHelper{
    private $adapter;

    /**
     * On construction create a new PDOAdapter
     */
    public function __construct() {
        $this->adapter = new PDOAdapter();
    }

   /**
    * [This function checks if the provided email is valid according to the type of user]
    * @param  [String] $user    [Type of user, vets or pet owners]
    * @param  [String] $p_email [Email]
    * @return [Array]          [Returns email, password & salt if valid, else null]
    */
    public function checkEmailQuery($user,$p_email){
        if($user == "vet"){
            $stmt = $this->adapter->conn->prepare(
                "SELECT email,pass,salt ".
                "FROM VETS ".
                "WHERE email=?;");
            $stmt->bindParam(1,$p_email);
            $result = null;
            try{
                $result = $this->adapter->executeFetchPrepared($stmt)[0];
            }catch(PDOException $e){
                return null;
            }
        
            return $result;
        }
        else if($user == "petOwner"){
            $stmt = $this->adapter->conn->prepare(
                "SELECT email,pass,salt ".
                "FROM PET_OWNER ".
                "WHERE email=?;");
            $stmt->bindParam(1,$p_email);
            $result = $this->adapter->executeFetchPrepared($stmt)[0];
            return $result;
        }
    }

    /**
     * Uses the PDO_Adapter to get the info 
     * for a specific vet by email
     * @param  String $p_email
     * @return Array
     */
    public function getVetInfoQuery($p_email){
        $stmt = $this->adapter->conn->prepare(
            "SELECT * FROM VETS WHERE email=?");
        $stmt->bindParam(1,$p_email);
       
        $result = null;
        try{
              $result = $this->adapter->executeFetchPrepared($stmt)[0];
        }catch(PDOException $e){
            return null;
        }
        
        return $result;
    }

    /** 
     * Uses the PDO_Adapter to get the info for a specific
     * pet by pet id and pet's birthday
     * @param  Integer p_pet_id
     * @return Array result
     */
    public function getPetInfoQuery($p_pet_id){
        $stmt = $this->adapter->conn->prepare(
            "SELECT * ".
            "FROM PET ".
            "WHERE pet_id = ?;");
        $stmt->bindParam(1,$p_pet_id);

        $result = null;
        try{
             $result = $this->adapter->executeFetchPrepared($stmt);
        }catch(PDOException $e){
            return null;
        }
        
        return $result;
    }
    
    /** NOT IMPLEMENTED CORRECTLY
     * Update a patient based on patient_id and clinic_id 
     * @param array p_patient
     * @param boolean
     */
    public function updatePatient($p_patient) {
        $stmt = $this->adapter->conn->prepare(
            "UPDATE PATIENT SET ".
            "name = ?, ".
            "sex = ?, ".
            "age = ?, ".
            "colour = ?, ".
            "breed = ?, ".
            "species = ?, ".
            "isNeutered = ? ".
            "WHERE patient_id = ? ".
            "AND ".
            "clinic_id = ?;");
        $stmt->bindParam(1,$p_patient['name']);
        $stmt->bindParam(2,$p_patient['sex']);
        $stmt->bindParam(3,$p_patient['age']);
        $stmt->bindParam(4,$p_patient['colour']);
        $stmt->bindParam(5,$p_patient['breed']);
        $stmt->bindParam(6,$p_patient['species']);
        $stmt->bindParam(7,$p_patient['isNeutered']);
        $stmt->bindParam(8,$p_patient['patient_id']);
        $stmt->bindParam(9,$p_patient['clinic_id']);
        $result = null;
        try{
            $result = $this->adapter->executeUpdatePrepared($stmt);
        }catch(PDOException $e){
            return false;
        }
        if($result > 0) {
            return true;
        }

        return false;
    }

    /** NOT IMPLEMENTED CORRECTLY
     * Create patient with information if clinic_id and patient_id is unique 
     * and name is not null.
     * @param  [array] $p_patient [of patient details]
     * @return bool            [true if inserted, false otherwise]
     */
    public function createPatient($p_patient) {
        $stmt = $this->adapter->conn->prepare(
            "INSERT INTO PATIENT VALUES(".
            "?,".
            "?,".
            "?,".
            "?,".
            "?,".
            "?,".
            "?,".
            "?,".
            "?);");
        $stmt->bindParam(1,$p_patient['name']);
        $stmt->bindParam(2,$p_patient['patient_id']);
        $stmt->bindParam(3,$p_patient['clinic_id']);
        $stmt->bindParam(4,$p_patient['sex']);
        $stmt->bindParam(5,$p_patient['age']);
        $stmt->bindParam(6,$p_patient['colour']);
        $stmt->bindParam(7,$p_patient['breed']);
        $stmt->bindParam(8,$p_patient['species']);
        $stmt->bindParam(9,$p_patient['isNeutered']);
        $result=null;
        try{
            $result = $this->adapter->executeUpdatePrepared($stmt);
        }catch(PDOException $e){
            return false;
        }
        if($result > 0) {
            return true;
        }

        return false;
    }

    /**
     * [Returns all interest info based on pet ID]
     * @param  [String] $p_pet_id [Pet ID]
     * @return [Array]  $result   [array of interest based on pet ID]
     */
    public function getAllInterestInfo($p_pet_id){
        $stmt = $this->adapter->conn->prepare(
            "SELECT * ".
            "FROM INTERESTS ".
            "WHERE pet_id=?;");
        $stmt->bindParam(1,$p_pet_id); 
        $result = null;

        try{
            $result = $this->adapter->executeFetchPrepared($stmt);
        }catch(PDOException $e){
            return null;
        }
        
        return $result;   
    }

    /**
     * [Returns all picture info based on pet ID]
     * @param  [String] $p_pet_id [Pet ID]
     * @return [Array]  $result   [array of pictures based on pet ID]
     */
    public function getAllPictureInfo($p_pet_id){
        $stmt = $this->adapter->conn->prepare(
            "SELECT * ".
            "FROM PICTURES ".
            "WHERE pet_id=?;");
        $stmt->bindParam(1,$p_pet_id);
        $result = null;
        try{
            $result = $this->adapter->executeFetchPrepared($stmt);
        }catch(PDOException $e){
            return null;
        }
        
        return $result; 
    }

    /**
     * Get all the clinic information from DB 
     *
     * Params:
     * Return Value: List of clinic info
     */
    public function getAllClinicInfo(){
        $stmt = $this->adapter->conn->prepare("SELECT * FROM CLINIC");  
        $result = null;
        try{
            $result = $this->adapter->executeFetchPrepared($stmt);
        }catch(PDOException $e){
            return null;
        }
        
        return $result;
    }

    /**
     *  update a clinic info 
     *  
     *  Params: clinic object
     *  Return Value:   true- row number is greater than zero
     *                  false- row number is zero or less
     */
    public function updateClinicInfo($p_clinic){ 

        $stmt = $this->adapter->conn->prepare("UPDATE CLINIC SET ".
        "clinic_name = ?, " . 
        "clinic_addr = ?, " .
        "post_code = ?, " .
        "latitude = ?, " .
        "longtitude = ?, " .
        "province = ?, " .
        "city = ?, " .
        "email = ?, " .
        "website = ?, " .
        "contact_person = ?, ".
        "active = ?, " .
        "expiration = ?, " .
        "WHERE clinic_id = ?;");

        $stmt->bindParam(1,$p_clinic->getClinicName());
        $stmt->bindParam(2,$p_clinic->getClinicAddress());
        $stmt->bindParam(3,$p_clinic->getPostCode());
        $stmt->bindParam(4,$p_clinic->getLatitude());
        $stmt->bindParam(5,$p_clinic->getLongtitude());
        $stmt->bindParam(6,$p_clinic->getProvince());
        $stmt->bindParam(7,$p_clinic->getCity());
        $stmt->bindParam(8,$p_clinic->getEmail());
        $stmt->bindParam(9,$p_clinic->getWebsite());
        $stmt->bindParam(10,$p_clinic->getContactPerson());
        $stmt->bindParam(11,$p_clinic->getActiveStatus());
        $stmt->bindParam(12,$p_clinic->getExpirationDate());
        $stmt->bindParam(13,$p_clinic->getClinicId());
        $result=null;
        try{
            $result = $this->adapter->executeUpdatePrepared($stmt);
        }catch(PDOException $e){
            return false;
        }
        if($result > 0) {
            return true;
        }

        return false;

    }

    /** NOT IMPLEMENTED PROPERLY, MAYBE NEEDED IN THE FUTURE
     * Get owner info
     * @param  [string] $p_clinic_id  [Clinic ID]
     * @param  [string] $p_patient_id [Patient ID]
     * @return [array]               [result of the select owner statement]
     */
    public function getOwnerInfo($p_clinic_id,$p_patient_id){
        $stmt = $this->adapter->conn->prepare("SELECT *,COUNT(*) as count FROM PATIENT_OWNER WHERE ".
            "clinic_id= ? AND ".
            "patient_id= ?;");
        $stmt->bindParam(1,$p_clinic_id);
        $stmt->bindParam(2,$p_patient_id);
        $result=null;
        return $result = $this->adapter->executeFetchPrepared($stmt)[0];
    }

     /**
     * Increment the likes count for a picture
     * @param  [ID] $p_pet_id [Pet ID]
     * @param  [ID] $p_pic_id [Pic ID]
     * @return [Bool]  [True or False depending on success]
     */
    public function updatePictureLikes($p_pet_id, $p_pic_id) {
        $stmt = $this->adapter->conn->prepare(
            "UPDATE PICTURES SET likes = likes + 1 ".  
            "WHERE pic_id=? and pet_id=?");
        $stmt->bindParam(1,$p_pic_id);
        $stmt->bindParam(2,$p_pet_id);
        $result=null;
        try{
            $result = $this->adapter->executeUpdatePrepared($stmt);
        }catch(PDOException $e){
            return false;
        }
        if($result > 0) {
            return true;
        }

        return false;
    }

     /**
     * Increment the views count for a picture
     * @param  [ID] $p_pet_id [Pet ID]
     * @param  [ID] $p_pic_id [Pic ID]
     * @return [Bool]  [True or False depending on success]
     */
    public function updatePictureViews($p_pet_id, $p_pic_id) {
        $stmt = $this->adapter->conn->prepare(
            "UPDATE PICTURES SET views = views + 1 ".  
            "WHERE pic_id=? and pet_id=?");
        $stmt->bindParam(1,$p_pic_id);
        $stmt->bindParam(2,$p_pet_id);

        $result=null;
        try{
            $result = $this->adapter->executeUpdatePrepared($stmt);
        }catch(PDOException $e){
            return false;
        }
        if($result > 0) {
            return true;
        }

        return false;
    }

    /** NOT IMPLEMENTED PROPERLY, MAY NEED IN THE FUTURE
     * Update patient owner with information if clinic_id and patient_id
     * is found
     * @param  [array] $p_patient_owner [Patient owner details]
     * @return [bool]            [true if updated, false otherwise]
     */
    public function updatePatientOwner($p_patient_owner) {
        $stmt = $this->adapter->conn->prepare(
            "UPDATE PATIENT_OWNER SET ".
            "firstname = ?,".
            "lastname = ?,".
            "address = ?,".
            "city = ?,".
            "province = ?,".
            "postal_code = ?,".
            "home_number = ?,".
            "cell_number = ?,".
            "email = ?,".
            "hasOptedIn = ? ".
            "WHERE clinic_id=? and patient_id = ? and owner_id = ?;");
        $stmt->bindParam(1,$p_patient_owner['firstname']);
        $stmt->bindParam(2,$p_patient_owner['lastname']);
        $stmt->bindParam(3,$p_patient_owner['address']);
        $stmt->bindParam(4,$p_patient_owner['city']);
        $stmt->bindParam(5,$p_patient_owner['province']);
        $stmt->bindParam(6,$p_patient_owner['postal_code']);
        $stmt->bindParam(7,$p_patient_owner['home_number']);
        $stmt->bindParam(8,$p_patient_owner['cell_number']);
        $stmt->bindParam(9,$p_patient_owner['email']);
        $stmt->bindParam(10,$p_patient_owner['hasOptedIn']);
        $stmt->bindParam(11,$p_patient_owner['clinic_id']);
        $stmt->bindParam(12,$p_patient_owner['patient_id']);
        $stmt->bindParam(13,$p_patient_owner['owner_id']);
        $result=null;
        try{
            $result = $this->adapter->executeUpdatePrepared($stmt);
        }catch(PDOException $e){
            return false;
        }
        if($result > 0) {
            return true;
        }
        return false;
    }

    /** 
     * Returns achievement Id if exist
     */
    public function checkAchievementId($p_achievement_id){
        $stmt = $this->adapter->conn->prepare(
            "SELECT achievement_id ".
            "FROM ACHIEVEMENT ".
            "WHERE achievement_id = ?;");
        $stmt->bindParam(1,$p_achievement_id);
        $result = $this->adapter->executeFetchPrepared($stmt);
        return $result;
    }

    /**
     * Returns achievement Id if exist
     */
    public function getAchievementRecordInfo($p_achievement_id, $p_pet_id){
        $stmt = $this->adapter->conn->prepare(
            "SELECT A.* , B.achievement_name, B.description". 
            " FROM ACHIEVEMENT_RECORD A join ACHIEVEMENT B on A.achievement_id = B.achievement_id".
            " WHERE A.achievement_id = ? and A.pet_id = ?;");

        $stmt->bindParam(1,$p_achievement_id);
        $stmt->bindParam(2,$p_pet_id);
        try{
             $result = $this->adapter->executeFetchPrepared($stmt);
        }catch(PDOException $e){
            return null;
        }
        return $result;
    }


    /**
     * [Insert a picture's info into the db]
     * @param [String] $p_pet_id      [The pet ID]
     * @param [String] $p_path        [The description of the picture]
     * @param [String] $pic_id [A unique picture ID]
     */
    public function addPicture($p_pet_id,$p_path,$p_description){
        $time = time();

        //Concat time witht pet ID = pic ID
        $pic_id = $time."_".$p_pet_id;

        //Insert into db
        $stmt = $this->adapter->conn->prepare(
            "INSERT INTO PICTURES".
            "(pet_id,pic_path,description,pic_id) ".
            "VALUES(".
            "?,".
            "?,".
            "?,".
            "?);");
        
        $stmt->bindParam(1,$p_pet_id);
        $stmt->bindParam(2,$p_path);
        $stmt->bindParam(3,$p_description);
        $stmt->bindParam(4,$pic_id);

        try{
            $result = $this->adapter->executeUpdatePrepared($stmt);
        }catch(PDOException $e){
            return null;
        }

        return $pic_id;
    }

    /** 
     * Update picture description with information if the picture
     * is found
     * @param  [array] $p_picture [Picture details]
     * @return [bool]            [true if updated, false otherwise]
     */
    public function updatePictureDescription($p_picture){

        $stmt = $this->adapter->conn->prepare(
            "UPDATE PICTURES ".
            "SET description = ? ".
            "WHERE pet_id = ? ".
            "AND ".
            "pic_id = ?;");
        $stmt->bindParam(1,$p_picture['description']);
        $stmt->bindParam(2,$p_picture['petId']);
        $stmt->bindParam(3,$p_picture['picId']);

        try{
            $result = $this->adapter->executeUpdatePrepared($stmt);
        }catch(PDOException $e){
            return false;
        }
        if($result > 0) {
            return true;
        }
        return false;
    }
    
    /**
     * Delete a picture through pet id and picture id
     * @param  [String] $p_petId $p_picId 
     * @return [bool]            [true if updated, false otherwise]
     */
    public function deletePicture($p_petId,$p_picId){
        $stmt = $this->adapter->conn->prepare(
            "DELETE FROM PICTURES ".
            "WHERE pet_id = ? ".
            "AND ".
            "pic_id = ?;");
        $stmt->bindParam(1,$p_petId);
        $stmt->bindParam(2,$p_picId);
        try{
            $result = $this->adapter->executeUpdatePrepared($stmt);
        }catch(PDOException $e){
            return false;
        }
        if($result > 0) {
            return true;
        }
        return false;
    }

}
?>
